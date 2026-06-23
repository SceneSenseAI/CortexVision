# CortexVision 🌍🧠

### Persistent World Modeling and Scene Understanding Framework

> Building machine perception systems that do not merely detect objects, but construct, maintain, reason over, and predict the state of the world.

---

# Overview

CortexVision is a research-oriented multimodal perception and world-modeling framework designed to move beyond traditional object detection and scene captioning.

Most computer vision systems process frames independently:

```text
Image
 ↓
Detector
 ↓
Bounding Boxes
```

CortexVision instead aims to build a persistent internal representation of reality:

```text
Video Stream
      ↓
Perception
      ↓
Scene Understanding
      ↓
World Modeling
      ↓
Memory
      ↓
Reasoning
      ↓
Prediction
```

The system continuously fuses detection, depth estimation, segmentation, tracking, temporal understanding, and scene graph generation to maintain a coherent understanding of dynamic environments.

---

# Core Research Question

> Can a machine construct and maintain a temporally consistent world model from monocular video streams using multimodal perception, scene graphs, memory, and predictive reasoning?

---

# Vision

Traditional vision systems answer:

> What objects exist?

CortexVision aims to answer:

> What exists, where is it, how is it changing, what is it interacting with, and what will happen next?

---

# System Architecture

```text
Video Stream
      │
      ▼

Perception Layer
 ├── YOLO-World
 ├── Depth Pro
 ├── SAM2
 ├── ByteTrack
 └── RTMPose

      │
      ▼

Fusion Layer
 ├── Detection Fusion
 ├── Depth Fusion
 ├── Object Association
 └── Scene Builder

      │
      ▼

Scene Graph Layer
 ├── Relation Extraction
 ├── Metric Scene Graph
 ├── Spatial Reasoning
 └── Graph Serialization

      │
      ▼

Memory Layer
 ├── Object Memory
 ├── Trajectory Store
 ├── Interaction Memory
 └── History Buffer

      │
      ▼

World Model Layer
 ├── Entity Store
 ├── World State
 ├── Event Engine
 └── Future Predictor

      │
      ▼

Navigation Layer
 ├── BEV Projection
 ├── Occupancy Grid
 ├── Corridor Detection
 └── Path Planning

      │
      ▼

Reasoning Layer
 ├── Temporal Understanding
 ├── VLM Reasoning
 ├── Event Explanation
 └── Future Prediction
```

---

# Key Components

## 1. Open-Vocabulary Detection

### Models

- YOLO-World
- Grounding DINO

### Purpose

Detect arbitrary objects beyond fixed label sets.

Examples:

```text
person
bicycle
helmet
wheelchair
traffic cone
```

---

## 2. Metric Depth Estimation

### Model

- Depth Pro

### Purpose

Estimate real-world spatial structure.

Example:

```text
Person: 2.1m away
Bicycle: 4.5m away
```

instead of:

```text
Person closer than bicycle
```

---

## 3. Segmentation

### Model

- SAM2

### Purpose

Provide precise object boundaries and spatial regions.

Outputs:

- object masks
- free-space regions
- scene structure

---

## 4. Tracking

### Model

- ByteTrack

### Purpose

Maintain persistent object identities.

Example:

```text
Frame 1 → Person #12
Frame 50 → Person #12
Frame 500 → Person #12
```

---

## 5. Depth Fusion

One of the primary research components.

Combines:

```text
Detection
+
Depth
+
Segmentation
```

to estimate:

```text
Object Distance
Object Position
3D Location
```

---

## 6. Metric Scene Graph Generation

A core contribution of CortexVision.

Example:

```text
Person
   │ 1.8m
   ▼
Bicycle
```

Relations include:

- left_of
- right_of
- in_front_of
- behind
- near
- overlapping
- contains

---

## 7. Object Memory

Unlike frame-based systems, CortexVision maintains memory.

Example:

```text
Person_12

Appeared
↓
Walking
↓
Approached Bicycle
↓
Mounted Bicycle
↓
Exited Scene
```

---

## 8. Temporal Scene Graphs

Tracks how relationships evolve over time.

Example:

```text
Person near bicycle
        ↓
Person touching bicycle
        ↓
Person riding bicycle
```

---

## 9. Future Event Prediction

The system predicts likely future interactions.

Examples:

- crossing road
- approaching obstacle
- entering corridor
- possible collision

---

## 10. Navigation Intelligence

Builds spatial representations suitable for robotics and assistive navigation.

Components:

- Bird's-Eye View projection
- Occupancy grid generation
- Free-path detection
- Safe route planning

---

# Research Contributions

## C1 — Depth-Aware Object Fusion

Object-centric spatial reasoning using metric depth estimation.

## C2 — Metric Scene Graph Generation

Spatially grounded graph construction from video streams.

## C3 — Persistent Object Memory

Long-term storage of object states and interactions.

## C4 — Temporal Scene Graph Evolution

Tracking relational changes through time.

## C5 — Predictive World Modeling

Future event forecasting from observed interactions.

## C6 — Navigation-Oriented Scene Understanding

Scene representations designed for path planning and robotics.

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