The core problem is that your current pipeline has about 18–22GB of model weight when everything is loaded together. That needs to come down to under 5GB of active model memory on an 8GB unified Jetson, leaving room for the OS, CUDA runtime, video buffers, and intermediate tensors.

Here's the full breakdown.

---

## Target Hardware Reality Check

**Jetson Orin NX 16GB** — best realistic target. 100 TOPS, 16GB unified memory (CPU + GPU share this), 25W. You'll hit 15–20 FPS end-to-end with the optimized stack below.

**Jetson Orin NX 8GB or Orin Nano 8GB** — harder but doable. 8GB unified is tight once the OS and CUDA runtime take ~3GB. You'll hit 8–12 FPS. The VLM must be completely optional/on-demand.

**RTX 3060 12GB or RTX 4060 8GB** — easier than Jetson because you have a separate CPU with its own RAM. Models sit in VRAM, system in RAM. 30–45 FPS achievable.

On Jetson specifically: there is no separate CPU RAM. Every byte of that 8GB or 16GB is shared between the ARM CPU, the GPU, and the OS. This is the single biggest constraint you need to design around.

---

## The Full Model Swap Table

```
Component       | Original             | Edge Version               | Memory (FP16)  | FPS (Orin NX 16GB)
----------------|----------------------|----------------------------|----------------|-------------------
Detection       | YOLO-World + GDINO   | YOLO-World-S + TensorRT    | ~45 MB         | ~40 FPS
Metric depth    | Depth Pro (ViT-L)    | DepthAnything V2-Small-M   | ~90 MB         | ~25 FPS
Segmentation    | SAM2 (ViT-H)         | NanoSAM (EfficientViT)     | ~55 MB         | ~30 FPS
Tracking        | ByteTrack            | ByteTrack (unchanged)      | ~5 MB          | >100 FPS
Pose            | RTMPose (133 kp)     | RTMPose-t + TensorRT       | ~10 MB         | ~60 FPS
Scene graph     | Large GNN            | Lightweight GCN (2-layer)  | ~10 MB         | >100 FPS
Temporal        | VideoMAE V2 (ViT-H)  | Keypoint LSTM              | ~5 MB          | >100 FPS
VLM             | InternVL2-8B         | Qwen2-VL-2B INT4 (async)   | ~1.4 GB        | ~2–3 FPS async
```

**Always-on model memory total: ~220 MB**
**With optional VLM loaded: ~1.6 GB**
**System + CUDA + buffers: ~2.5–3 GB**
**Total on 8GB device: ~4.5–5 GB → feasible with 3GB headroom**

---

## Why Each Model Was Swapped

**Depth Pro → DepthAnything V2 Small Metric**

Depth Pro uses a ViT-L backbone (307M params). Way too heavy. DepthAnythingV2-Small uses a ViT-S backbone (25M params) and has a metric variant fine-tuned on NYUv2 for indoor absolute depth. You lose some boundary sharpness but the metric accuracy for navigation is still solid. Export to TensorRT FP16.

**SAM2 → NanoSAM**

NanoSAM is NVIDIA's own edge-optimized SAM variant built for Jetson. It uses an EfficientViT backbone and is distributed as a pre-built TensorRT engine. SAM2 takes ~500ms per mask on Jetson; NanoSAM takes ~14ms. It ships with example code specifically for Jetson Orin. This is not a compromise — it's the right tool.

**VideoMAE V2 → Keypoint LSTM**

This is the most important architectural change. VideoMAE V2 is a ViT-H model with ~600M parameters. On Jetson, it would take 3–5GB alone and run at 0.5 FPS. You already have 133 keypoints per person per frame from RTMPose. Feed a sliding window of 16–30 keypoint frames into a small LSTM or 1D-CNN (< 1M parameters). You get action classification from skeleton sequences at essentially zero cost. ST-GCN (Spatial-Temporal GCN) is the research-grade version of this approach — it's what PoseC3D and most modern skeleton action recognition papers use. This is actually a better research contribution than VideoMAE V2 because it's explainable.

**InternVL2-8B → Qwen2-VL-2B INT4 (on-demand only)**

8 billion parameters will not coexist with the rest of your pipeline on 8GB unified memory. Qwen2-VL-2B quantized to INT4 takes ~1.4GB. Load it on-demand when triggered by scene change events or user queries. Unload when done. moondream2 (1.86B) is another option — it's the lightest capable VLM and was specifically designed for constrained deployment.

---

## Modified Pipeline Architecture

```
Camera (V4L2 / CSI) 
    |
    | NVDEC hardware decode (no CPU copy)
    | NV12 format directly to GPU
    |
Async Ring Buffer (CUDA pinned memory, 4–8 frames)
    |
    +------ Detection thread    --> YOLO-World-S (TRT INT8)   --> detections
    |
    +------ Depth thread        --> DAV2-Small-M (TRT FP16)  --> depth map
    |
    +------ Segmentation thread --> NanoSAM (TRT FP16)       --> masks
    |
[NOT ALL EVERY FRAME: depth + seg run every 2nd frame, detection every frame]
    |
Depth-to-Object Fusion (CUDA kernel: sample depth at mask centroid)
    |
ByteTrack (CPU, trivial cost)
    |
    +------ Pose thread  --> RTMPose-t (TRT FP16) --> 133 keypoints per person
    |
    +------ Scene Graph  --> Lightweight 2-layer GCN --> spatial relations
    |
Temporal: ST-GCN or LSTM on keypoint window --> action labels
    |
    +------ JSON scene dict (always-on output)
    |
    +------ Gradio dashboard (always-on output)
    |
    +------ VLM (Qwen2-VL-2B INT4) [ASYNC, event-triggered only]
                 triggered by: scene change > threshold
                              user voice/text query
                              anomaly detection flag
```

---

## Frame Skipping Strategy

Not everything needs to run every frame. This is the key insight for real-time edge performance.

```
Every frame (30 FPS input):
    Detection with YOLO-World-S

Every 2nd frame:
    Depth estimation with DAV2-Small-M
    Segmentation with NanoSAM
    (use previous frame depth/masks for the skipped frame)

Every 3rd frame:
    Scene graph update
    Pose estimation (unless a person was just detected, then every 2nd)

Every Nth frame (N based on scene stability score):
    VLM narration (only if scene changed significantly)
    Typically every 2–5 seconds, not every frame
```

This gives you effectively 30 FPS detection with 15 FPS depth and 10 FPS scene graph updates. For navigation assistance this is more than sufficient.

---

## TensorRT Conversion Plan

Every model needs to be converted to a TensorRT engine before deployment. Do this once on the device or cross-compile on x86.

```
Step 1: Export PyTorch → ONNX
    torch.onnx.export(model, dummy_input, "model.onnx",
                      opset_version=17,
                      input_names=["input"],
                      output_names=["output"],
                      dynamic_axes={"input": {0: "batch"}})

Step 2: ONNX → TensorRT engine
    trtexec --onnx=model.onnx \
            --saveEngine=model.engine \
            --fp16 \
            --workspace=2048 \
            --input-shapes=input:1x3x640x640

    For INT8 (detection only, needs calibration data):
    trtexec --onnx=yolo.onnx \
            --saveEngine=yolo_int8.engine \
            --int8 \
            --calib=calib_cache.bin \
            --workspace=4096

Step 3: Load engine at runtime
    with open("model.engine", "rb") as f:
        engine = runtime.deserialize_cuda_engine(f.read())
    context = engine.create_execution_context()
```

Use `torch2trt` as an easier wrapper if you prefer Python over trtexec.

---

## Memory Management on Jetson

The Jetson unified memory architecture means you need to be careful about memory pinning and zero-copy transfers.

```python
# Pinned memory allocation (avoids CPU-GPU copy overhead)
input_buffer = cuda.pagelocked_empty((1, 3, 640, 640), dtype=np.float32)

# CUDA streams for async execution
detection_stream = cuda.Stream()
depth_stream = cuda.Stream()
seg_stream = cuda.Stream()

# Run detection and depth simultaneously on different streams
context_det.execute_async_v2(det_bindings, detection_stream.handle)
context_depth.execute_async_v2(depth_bindings, depth_stream.handle)

# Synchronize only when you need the results
detection_stream.synchronize()
depth_stream.synchronize()
```

For NanoSAM specifically, NVIDIA provides a Jetson-ready interface that handles this internally. Use their example code as the starting point.

---

## JetPack Setup Checklist

```
JetPack version: 6.0 or 6.1 (Ubuntu 22.04 base)
CUDA: 12.2
TensorRT: 8.6.2 or later
cuDNN: 8.9+
Python: 3.10
PyTorch: 2.1.0 (Jetson wheel from NVIDIA, NOT pip install torch)
torchvision: matching Jetson wheel

Power mode:
    sudo nvpmodel -m 0        # max power mode
    sudo jetson_clocks         # lock clocks to max

Check available memory before loading models:
    tegrastats                 # real-time memory + GPU usage
    jtop                       # better dashboard (pip install jetson-stats)
```

Install order matters on Jetson. Install JetPack components first, then PyTorch from NVIDIA's wheel repository, then everything else. Do not use `pip install torch` — it will pull an x86 binary that will not work.

---

## Replacing VideoMAE V2 with ST-GCN (the right way)

This is the architecture change that matters most for edge and for research quality.

```
Input: 
    RTMPose output → 133 keypoints × (x, y, confidence) per frame
    Window of 30 frames → shape (30, 133, 3)

ST-GCN graph:
    Nodes: keypoints (133)
    Edges: human body connectivity (COCO-WholeBody skeleton)
    Temporal edges: same keypoint across consecutive frames

Model size:
    ST-GCN with 128-dim hidden → ~2M params → ~8MB at FP16
    Inference: 1–2ms on Jetson GPU

Output:
    Action labels (walk, sit, stand, gesture, fall, etc.)
    Confidence scores

Training:
    Pretrain on NTU RGB+D or Kinetics-Skeleton
    Fine-tune on your IIT Patna keypoint sequences

Research framing:
    "Skeleton-based action recognition from monocular video
     for real-time scene understanding on edge hardware"
    This is cleaner, more explainable, and more citable
    than a black-box VideoMAE prediction
```

ST-GCN is published (AAAI 2018), well-cited, and has solid PyTorch implementations. Your contribution is using it as the temporal backbone of a metric scene understanding pipeline rather than as a standalone action recognition system.

---

## VLM Strategy on Edge: Event-Triggered, Not Per-Frame

```
Scene change detector (runs every frame, trivial cost):
    compare current scene graph hash to previous
    if (new objects added) or (relations changed > threshold):
        trigger_vlm_event = True

VLM worker thread (separate process):
    while running:
        wait for trigger_vlm_event
        load Qwen2-VL-2B INT4 if not loaded (lazy load)
        run inference on current frame + scene graph JSON
        output narration string
        if no new events for 60 seconds:
            unload model to free memory

Result: VLM runs ~2–3 times per minute during typical use
        instead of 30 times per second
        Saves 1.4GB of always-on memory
```

For wearable/assistive use, this is actually better UX. Constant narration is annoying. Event-triggered narration ("a person just sat down near the whiteboard") is useful.

---

## Expected Performance Numbers

```
Hardware: Jetson Orin NX 16GB, JetPack 6.1, TRT FP16/INT8, 640×480 input

Stage                     | Latency    | Effective FPS
--------------------------|------------|---------------
YOLO-World-S (INT8)       | 12 ms      | ~83 FPS (not bottleneck)
DepthAnythingV2-S (FP16)  | 28 ms      | ~35 FPS (runs every 2nd frame → 17 FPS effective)
NanoSAM (FP16)            | 14 ms      | ~70 FPS (runs every 2nd frame)
ByteTrack (CPU)           | 2 ms       | >100 FPS
RTMPose-t (FP16)          | 8 ms       | ~125 FPS
Lightweight GCN           | 1 ms       | >200 FPS
ST-GCN action (FP16)      | 2 ms       | >100 FPS
Pipeline total (async)    | ~35–40 ms  | 15–20 FPS end-to-end

Hardware: Jetson Orin Nano 8GB

Pipeline total (async)    | ~70–80 ms  | 8–12 FPS end-to-end
```

---

## Repository Changes Needed

```
New directory: deployment/
    trt_engines/           # store converted .engine files
    convert_models.py      # one-time conversion script
    edge_config.yaml       # edge-specific model paths + quantization settings
    benchmark.py           # FPS + latency profiler per stage

Replace in models/:
    depth/depth_estimator.py      → point to DAV2-Small-M + TRT backend
    segmentation/segmentor.py     → point to NanoSAM + TRT backend
    pose/pose_estimator.py        → RTMPose-t + TRT backend
    temporal/action_recogniser.py → ST-GCN or Keypoint LSTM
    temporal/video_understander.py → DELETE (VideoMAE V2 is gone)
    vlm/local_vlm.py              → Qwen2-VL-2B INT4, lazy load

New in app/:
    edge_pipeline.py       # frame-skip-aware pipeline replacing pipeline.py
    memory_manager.py      # track GPU memory, trigger VLM load/unload

New in configs/:
    edge.yaml              # all edge-specific overrides
```

---

## Implementation Priority for Edge

1. Get JetPack 6.x running with jtop confirming GPU access
2. Convert YOLO-World-S to TensorRT INT8 and verify detection works
3. Convert DepthAnythingV2-Small-Metric to TRT FP16 and verify metric output
4. Set up NanoSAM from NVIDIA's official Jetson example
5. Wire ByteTrack + depth fusion on top of these three
6. Add RTMPose-t in TRT FP16
7. Replace VideoMAE V2 with ST-GCN on keypoint sequences — test action labels
8. Implement lightweight GCN scene graph with metric depth edges
9. Add event-triggered Qwen2-VL-2B INT4 as async worker
10. Profile end-to-end with `tegrastats` and `nvidia-smi dmon`, tune frame skip rates

Steps 1–4 will take the longest. Once TensorRT conversion is working reliably for one model, the rest follow the same pattern.