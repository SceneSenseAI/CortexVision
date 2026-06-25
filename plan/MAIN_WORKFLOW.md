## Updated SceneSenseAI Workflow

---

### The Pipeline (in order)

**Stage 1 — Input**
Webcam, video file, or RTSP stream feeds into an async ring buffer. FPS is controlled here, frames are GPU pre-loaded. Nothing downstream blocks on I/O.

**Stage 2 — Async Frame Buffer**
The ring buffer holds recent frames and dispatches the current frame in parallel to all three perception models simultaneously. This is the async orchestrator you need to write yourself — it's where your CV claim lives.

**Stage 3 — Perception Layer (3 threads, parallel)**
Three models run at the same time on the same frame:

- Detection: YOLO-World handles real-time open-vocabulary detection. GDINO 1.5 runs offline for accuracy benchmarks only. Do not run GDINO in the real-time loop.
- Metric depth: Depth Pro (Apple, Sep 2024) replaces DepthAnything V2. Key difference: Depth Pro gives absolute depth in meters without needing scene calibration. This is what makes your scene graph metric-aware rather than just topological.
- Segmentation + tracking: SAM2 handles both video segmentation and temporal consistency in one pass.

**Stage 4 — Tracking + Depth Fusion**
ByteTrack assigns persistent IDs across frames. Each stable ID gets a metric depth value sampled from Depth Pro's depth map at the mask centroid. Result: every tracked object now carries a real-world distance from the camera.

**Stage 5 — Understanding Layer (2 branches, parallel)**
From the fused detections:

- RTMPose estimates human pose (133 keypoints, 30+ FPS on CPU). Feeds into action classification.
- Metric Scene Graph (GNN-based): this is your core research contribution. Nodes are tracked objects with metric positions. Edges are spatial relations (next-to, in-front-of, on-top-of) weighted by actual distances in meters. Compare this against standard SGG literature (RelTR, EGTR) which gives only topological relations with no real-world scale.

**Stage 6 — Temporal: VideoMAE V2**
Takes the scene + pose across a sliding window of frames. Outputs action labels and activity classifications. This replaces both RAFT optical flow and a separate action model — VideoMAE V2 collapses those three EPICs into one backbone.

**Stage 7 — Research Outputs (3 branches)**

- Temporal Scene Graph: EMA-smoothed relations across frames using stable ByteTrack IDs. Most SGG papers work per-image. Video SGG that handles flickering with temporal smoothing is your second contribution. Proposed metric: edge consistency rate across a sliding window.
- BEV + Free Corridor: Depth Pro metric depth + SAM2 segmentation masks → bird's-eye view map → navigable path extraction. From a single uncalibrated monocular camera. This is the applied output — assistive AI, indoor navigation, robotics.
- InternVL2-8B VLM: local inference only. Cloud VLMs (Claude, GPT-4o) run offline for eval and ablation, never in the inference loop.

---

### What Was Dropped and Why

**Audio module** (audio_event.py, speech_recogniser.py, vl_aligner.py): separate research field, zero contribution to scene understanding, dilutes your thesis. Delete the folder entirely.

**CIFAR-10 and FashionMNIST**: tutorial exercises with no connection to this project. Move them to a separate learning repo if you want, but remove from this one.

**RAFT optical flow**: VideoMAE V2 captures temporal motion implicitly. RAFT added ~50ms latency for no measurable gain once VideoMAE is in the stack.

**Cloud VLMs in the inference loop**: API cost compounds dangerously in real-time. Claude and GPT-4o stay for offline evaluation and ablation studies only.

**Sentinel mode as a product**: keep it as a deployment config flag, not a separate codebase. One pipeline, multiple output modes.

**Wearable as a separate product**: same as above. The BEV + TTS path is just one output mode of the same pipeline.

---

### Model Upgrades

**Depth Anything V2 → Depth Pro.** Both give metric depth, but Depth Pro has sharper object boundaries and better zero-shot generalization across indoor environments. Most importantly, it gives absolute scale without scene-level calibration — which is what makes your metric scene graph a real research contribution rather than a relative-depth approximation.

**Add MLflow from day one.** Every FPS measurement, config parameter, and eval score gets logged. Your paper figures come directly from these logs. This is not optional if you want a publishable result.

**Benchmark InternVL2-8B against MiniCPM-V 2.6.** MiniCPM-V is smaller and faster — potentially better for edge deployment and the wearable output mode.

---

### The Four Research Contributions

**1. Metric Scene Graph Generation** is your primary contribution. Standard scene graph generation (Visual Genome, GQA) gives topological relations: "person — riding — horse". Your system encodes real-world distances: "person (1.2m) — next-to — chair (1.5m) — facing — whiteboard (3.2m)". Every edge carries a spatial measurement derived from Depth Pro. Compare against depth-free SGG baseline and relative-depth baseline in ablation.

**2. Temporal Scene Graph Stability** is your second contribution. Most SGG papers are per-image. Your contribution is using ByteTrack stable IDs plus EMA-smoothed relation confidences to produce consistent scene graphs across frames. Measurable metric: edge consistency rate (fraction of edges that remain consistent over a sliding window of N frames).

**3. BEV + Navigable Path Detection** is your applied contribution. Depth Pro + SAM2 → bird's-eye view → free corridor detection from a single monocular camera. Very few systems achieve this without stereo or LiDAR. Evaluate with corridor detection F1 on annotated IIT Patna sequences.

**4. IIT Patna Scene Dataset** is your dataset contribution. Annotate it for scene graph relations, not just bounding boxes. Classroom, corridor, cafeteria, road, and night scenes from an Indian academic environment fills a real gap — most SGG datasets are single-image web photos. Release it publicly.

---

### Ablation Studies (what makes it a paper)

Run four ablations on the IIT Patna dataset:
- Without metric depth (topological SGG only, no distances)
- Without temporal smoothing (per-frame SGG, no EMA)
- Without pose estimation (scene graph only)
- Depth Pro vs DepthAnything V2 (justify your model choice quantitatively)

---

### Implementation Priority

Phase 1 — delete everything listed above, upgrade to Depth Pro, wire up MLflow.
Phase 2 — implement the GNN scene graph with metric depth fusion. This is where 70% of your time should go.
Phase 3 — evaluation suite on IIT Patna, get baseline numbers.
Phase 4 — temporal SGG + BEV navigation.
Phase 5 — paper writeup.

---

### Resume Line

"Built SceneSenseAI: real-time metric scene graph generation using Depth Pro, YOLO-World, SAM2, and a GNN-based relation inference layer. Curated IIT Patna Scene Dataset across 5 environments with scene graph annotations. Achieved [X]% temporal edge consistency and [Y]% corridor detection F1 at [Z] FPS on RTX 3090."

### Paper Title

"Towards Metric-Aware Video Scene Graphs for Indoor Navigation Assistance" — target ECCV 2026, ICCV workshop on scene understanding, or IROS 2025 for the robotics angle. The IIT Patna dataset alone could go to NeurIPS 2025 dataset track.