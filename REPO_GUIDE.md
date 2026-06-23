# CortexVision

> A Research-Oriented Multimodal Scene Understanding and World Modeling Framework

CortexVision is an advanced perception and reasoning system designed to move beyond traditional object detection and toward persistent scene understanding.

Unlike conventional computer vision pipelines that operate on individual frames, CortexVision constructs a dynamic internal representation of the environment by combining:

- Open-Vocabulary Object Detection
- Metric Depth Estimation
- Object Tracking
- Scene Graph Generation
- Temporal Memory
- World Modeling
- Future Event Prediction
- Vision-Language Reasoning

The long-term goal is to enable machines to understand and reason about dynamic real-world environments in a manner closer to human perception.

---

# System Architecture

```text
Video Stream
      │
      ▼
Perception Layer
 ├── Detection
 ├── Depth
 ├── Segmentation
 ├── Tracking
 └── Pose Estimation
      │
      ▼
Fusion Layer
 ├── Depth Fusion
 ├── Object Association
 └── Scene Builder
      │
      ▼
World Modeling Layer
 ├── Metric Scene Graph
 ├── Object Memory
 ├── World State
 └── Event Engine
      │
      ▼
Temporal Understanding
 ├── Temporal Scene Graph
 ├── Activity Understanding
 └── Future Prediction
      │
      ▼
Reasoning Layer
 ├── Graph Reasoning
 ├── VLM Explanation
 └── Navigation Planning
```

---

# Repository Structure

```text
CortexVision/
│
├── app/
├── benchmarks/
├── checkpoints/
├── configs/
├── core/
├── datasets/
├── docs/
├── evaluation/
├── experiments/
├── models/
├── notebooks/
├── outputs/
├── paper/
├── scripts/
├── tests/
├── tools/
└── utils/
```

---

# Core Components

## `core/`

Contains the canonical data structures shared throughout the system.

### `frame.py`

Represents an input frame and associated metadata.

### `object.py`

Defines the primary representation of detected entities.

Example:

```python
SceneObject(
    id=12,
    label="person",
    confidence=0.95,
    depth=3.4
)
```

### `scene.py`

Represents a complete scene at a specific timestamp.

### `trajectory.py`

Stores temporal movement information.

### `event.py`

Represents detected interactions and events.

### `world_state.py`

Maintains the persistent world representation.

---

# Perception Layer

## Detection

**Location**

```text
models/detection/
```

### Models

- YOLO-World
- Grounding DINO

### Output

```json
{
  "class": "person",
  "bbox": [x1, y1, x2, y2]
}
```

---

## Depth Estimation

**Location**

```text
models/depth/
```

### Model

- Depth Pro

### Output

```json
{
  "depth": 3.7
}
```

---

## Segmentation

**Location**

```text
models/segmentation/
```

### Model

- SAM2

### Output

Pixel-level object masks.

---

## Tracking

**Location**

```text
models/tracking/
```

### Components

#### `tracker.py`

Maintains stable object identities.

#### `depth_fusion.py`

Combines:

- Detections
- Masks
- Depth Maps

to estimate object-level depth and 3D positions.

#### `object_association.py`

Associates detections across frames.

#### `track_state.py`

Stores track lifecycle information.

---

## Pose Estimation

**Location**

```text
models/pose/
```

### Model

- RTMPose

### Output

Human body keypoints.

---

# Scene Graph Layer

## `models/scene_graph`

This is the primary research component of CortexVision.

### `relation_extractor.py`

Extracts relationships such as:

- left_of
- right_of
- behind
- in_front_of
- overlapping
- contains

---

### `metric_scene_graph.py`

Constructs spatially-aware scene graphs using metric depth.

Example:

```text
Person
  │ 2.3m
  ▼
Bicycle
```

---

### `temporal_scene_graph.py`

Tracks graph evolution across time.

Example:

```text
Approaching
     ↓
Interacting
     ↓
Leaving
```

---

### `spatial_reasoner.py`

Performs graph-based reasoning.

---

### `graph_serializer.py`

Exports graphs into JSON and benchmark formats.

---

# Memory Layer

## `models/memory`

Maintains long-term object history.

### `trajectory_store.py`

Stores object trajectories.

### `history_buffer.py`

Maintains temporal observations.

### `interaction_memory.py`

Records interactions.

Example:

```text
Person_12
 ├── Appeared
 ├── Walking
 ├── Near Bicycle
 ├── Mounted Bicycle
 └── Left Scene
```

---

# World Model Layer

## `models/world_model`

Represents CortexVision's internal understanding of reality.

### `object_memory.py`

Persistent object memory.

### `entity_store.py`

Stores all active entities.

### `world_state.py`

Maintains the current world representation.

### `event_engine.py`

Generates semantic events.

### `future_predictor.py`

Predicts future actions and interactions.

Examples:

- Crossing Road
- Approaching Obstacle
- Entering Corridor
- Potential Collision

---

# Navigation Layer

## `models/navigation`

### `bev_projection.py`

Projects observations into Bird's-Eye View.

### `occupancy_grid.py`

Builds navigable occupancy maps.

### `corridor_detector.py`

Detects traversable free-space corridors.

### `path_planner.py`

Computes safe navigation routes.

---

# Temporal Understanding

## `models/temporal`

### `action_recogniser.py`

Recognizes atomic actions.

### `activity_detector.py`

Detects longer activities.

### `video_understander.py`

Extracts temporal context from videos.

---

# Vision-Language Layer

## `models/vlm`

### `local_vlm.py`

Runs local Vision-Language Models.

### `cloud_vlm.py`

Interfaces with cloud-based VLM APIs.

Applications include:

- Scene Explanation
- Question Answering
- Semantic Reasoning
- Natural Language Summaries

---

# Application Layer

## `app/`

Contains orchestration and pipeline logic.

### `pipeline.py`

Main processing pipeline.

### `scene_builder.py`

Creates structured scene representations.

### `world_model_builder.py`

Updates world state.

### `object_memory_manager.py`

Maintains persistent memory.

### `event_detector.py`

Detects semantic events.

### `bev_builder.py`

Constructs Bird's-Eye View representations.

### `scene_explainer.py`

Generates natural language scene explanations.

---

# Evaluation

## `evaluation/`

Measures system performance.

### Core Metrics

| Metric | Purpose |
|----------|----------|
| scene_graph_precision | Scene graph quality |
| graph_consistency | Structural correctness |
| graph_temporal_stability | Temporal consistency |
| object_persistence | Tracking stability |
| trajectory_consistency | Trajectory reliability |
| world_model_accuracy | World state quality |
| prediction_accuracy | Future prediction quality |
| navigation_success | Navigation performance |
| latency | Runtime efficiency |
| fps | Throughput |

---

# Benchmarks

## `benchmarks/`

Contains benchmark specifications and evaluation protocols.

### Current Benchmarks

- Metric Scene Graph Generation
- Temporal Scene Graph Generation
- Navigation Performance

---

# Research Roadmap

## Phase 1

- Detection
- Depth Estimation
- Tracking
- Depth Fusion

## Phase 2

- Metric Scene Graph Generation

## Phase 3

- Persistent Object Memory

## Phase 4

- Temporal Scene Graphs

## Phase 5

- Future Event Prediction

## Phase 6

- Navigation and World Reasoning

---

# Long-Term Vision

CortexVision aims to evolve from a scene understanding system into a complete world-modeling framework capable of:

- Persistent Environmental Understanding
- Human Activity Comprehension
- Event Prediction
- Navigation Assistance
- Robotic Perception
- Embodied AI Reasoning

The ultimate objective is to build systems that understand dynamic environments rather than merely detect objects within them.

---

# Key Research Contributions

The primary novelty of CortexVision lies in:

1. Metric Scene Graph Generation
2. Persistent Object Memory
3. Temporal Scene Graph Evolution
4. World State Construction
5. Future Event Prediction
6. Navigation-Oriented Scene Understanding

Rather than treating each frame independently, CortexVision maintains a continuously evolving world model capable of supporting long-term reasoning and prediction.