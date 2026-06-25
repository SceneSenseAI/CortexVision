# MLflow Usage Guide (SceneSenseAI / CortexVision)

## Purpose

MLflow is the experiment tracking framework for the project.

It records:

- Experiment configurations
- Parameters
- Metrics
- Artifacts
- Trained models
- Experiment history

Think of MLflow as your **digital research notebook**.

---

# Workflow

```text
Write Code
      │
      ▼
Run Experiment
      │
      ▼
MLflow Logs Everything
      │
      ▼
Compare Results
      │
      ▼
Improve Model
      │
      ▼
Repeat
```

---

# Step 1 — Start MLflow

Run the MLflow UI from the project root.

```bash
mlflow ui
```

Open:

```
http://127.0.0.1:5000
```

Leave it running while performing experiments.

---

# Step 2 — Import the Logger

```python
from utils.mlflow_logger import MLFlowLogger
```

---

# Step 3 — Create the Logger

```python
logger = MLFlowLogger()
```

Only one logger is required per experiment.

---

# Step 4 — Start a New Run

Every meaningful experiment should have its own run.

```python
logger.start_run("Detection Benchmark")
```

### Example Run Names

- Detection Benchmark
- Depth Benchmark
- Segmentation Benchmark
- Tracking Benchmark
- Pose Benchmark
- Metric Scene Graph
- Temporal Scene Graph
- Navigation Benchmark
- World Model
- Ablation - Without Depth
- Ablation - Without Pose
- Ablation - Without Temporal
- Final Pipeline

---

# Step 5 — Log Parameters

Parameters describe **how the experiment was executed**.

Log them immediately after starting the run.

```python
logger.log_params({

    "Detector": "YOLO-World",

    "Depth": "Depth Pro",

    "Segmentation": "SAM2",

    "Tracker": "ByteTrack",

    "Pose": "RTMPose",

    "Resolution": 640,

    "Device": "RTX4060",

    "Precision": "FP16"

})
```

## Typical Parameters

- Detector
- Depth Model
- Segmentation Model
- Tracker
- Pose Model
- Resolution
- Batch Size
- Confidence Threshold
- Device
- Precision
- Dataset
- Frame Skip
- Temporal Window

---

# Step 6 — Execute the Experiment

Run the pipeline normally.

Example:

```python
objects = detector.detect(frame)

tracks = tracker.track(objects)

scene = scene_builder.build(frame, tracks)

world_state = world_model.update(scene)
```

> **Important**
>
> Do **NOT** use MLflow inside:
>
> - detector.py
> - tracker.py
> - depth_estimator.py
> - segmentor.py
> - scene_graph.py
> - world_model.py
>
> These modules should only perform inference.

---

# Step 7 — Compute Metrics

Evaluation modules compute the metrics.

Example:

```python
metrics = {

    "FPS": 32.4,

    "Latency": 24.6,

    "Objects": 8,

    "Scene Graph Precision": 0.91,

    "Temporal Stability": 0.94

}
```

---

# Step 8 — Log Metrics

```python
logger.log_metrics(metrics)
```

or

```python
logger.log_metric("FPS", fps)

logger.log_metric("Latency", latency)
```

---

# Step 9 — Log Artifacts

Artifacts are files generated during the experiment.

Examples:

- Images
- Videos
- JSON files
- CSV files
- Confusion Matrices
- BEV Maps
- Graph Visualizations
- Plots

Example:

```python
logger.log_artifact("outputs/output.mp4")

logger.log_artifact("outputs/scene_graph.json")

logger.log_artifact("outputs/bev.png")

logger.log_artifact("paper/plots/fps_curve.png")
```

---

# Step 10 — Log Models (Training Only)

Only required when training a model.

```python
logger.log_pytorch_model(model)
```

Examples:

- ST-GCN
- Scene Graph GNN
- Future Predictor
- Fine-tuned Models

---

# Step 11 — End the Run

```python
logger.end_run()
```

Always end every experiment with `end_run()`.

---

# Complete Example

```python
from utils.mlflow_logger import MLFlowLogger

logger = MLFlowLogger()

logger.start_run("Detection Benchmark")

logger.log_params({

    "Detector": "YOLO-World",

    "Resolution": 640,

    "Device": "RTX4060"

})

# Run experiment

fps = 32.6
latency = 21.4

logger.log_metrics({

    "FPS": fps,

    "Latency": latency

})

logger.log_artifact("outputs/output.mp4")

logger.end_run()
```

---

# Project Workflow

```text
Experiment Script
        │
        ▼
Start Run
        │
        ▼
Log Parameters
        │
        ▼
Run Pipeline
        │
        ▼
Compute Metrics
        │
        ▼
Log Metrics
        │
        ▼
Log Artifacts
        │
        ▼
End Run
```

---

# Where to Use MLflow

Use MLflow for:

- Benchmarking
- Ablation studies
- Model comparison
- Hyperparameter tuning
- Final evaluation
- Paper experiments

Do **NOT** use MLflow for:

- Unit tests
- Debugging
- Individual model implementations

---

# Repository Structure

```
CortexVision/

configs/
    mlflow.yaml

utils/
    mlflow_logger.py

experiments/
    01_detection/
    02_depth/
    03_scene_graph/
    04_world_model/
    08_ablations/

evaluation/

outputs/

artifacts/

mlflow.db
```

---

# Best Practices

✅ One run = One experiment

✅ Log parameters immediately after starting the run

✅ Log metrics after evaluation

✅ Log generated artifacts

✅ Use descriptive run names

✅ Compare runs through the MLflow UI

❌ Don't call MLflow inside model modules

❌ Don't create a new run for every debugging attempt

❌ Don't mix multiple experiments into one run