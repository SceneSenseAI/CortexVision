```
<div align="center">

<br />

```
█▀▀ █▀█ █▀█ ▀█▀ █▀▀ ▀▄▀   █░█ █ █▀ █ █▀█ █▄░█
█▄▄ █▄█ █▀▄ ░█░ ██▄ █░█   ▀▄▀ █ ▄█ █ █▄█ █░▀█
```

**Persistent World Modeling · Scene Understanding · Predictive Intelligence**

<br />

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research-orange?style=flat-square)]()
[![IIT Patna](https://img.shields.io/badge/IIT%20Patna-CSE-purple?style=flat-square)]()

<br />

> *Most vision systems see frames. CortexVision builds worlds.*

<br />

</div>

---

## What is this?

Standard computer vision answers one question: **what objects are in this frame?**

CortexVision asks something harder:

> **What exists, where is it, how is it changing, what is it interacting with — and what will happen next?**

This is a research framework for **persistent world modeling from monocular video** — fusing detection, depth, segmentation, tracking, and language reasoning into a continuously-updated internal representation of reality. Not a frame-by-frame pipeline. A machine that *remembers*, *reasons*, and *predicts*.

---

## The Gap This Fills

```
Traditional Vision                    CortexVision
─────────────────                     ────────────

Frame → Detector → Boxes              Video Stream
                                           │
[Frame 1]  [person]                        ▼
[Frame 2]  [person]              Perception + Fusion
[Frame 3]  [person]                        │
                                           ▼
No memory. No continuity.          Scene Graph + Memory
No depth. No relationships.                │
No prediction.                             ▼
                                    World Model + Events
                                           │
                                           ▼
                                  Navigation + Prediction
```

---

## Architecture

The system is organized as a deep processing stack — each layer feeds the next, building richer understanding at every stage.

### Layer 1 — Perception

Raw video in. Five specialized models run in parallel:

| Model | Role |
|---|---|
| `YOLO-World` | Open-vocabulary object detection — detect anything, not just fixed classes |
| `Depth Pro` | Metric depth estimation — real distances in meters, not relative ordering |
| `SAM2` | Pixel-precise segmentation — object masks and free-space regions |
| `ByteTrack` | Multi-object tracking — persistent identities across hundreds of frames |
| `RTMPose` | Pose estimation — body keypoints for humans |

### Layer 2 — Fusion

Where the magic starts. Detection, depth, and segmentation are fused per-object to produce:

- **Metric 3D position** — not "person is closer than bicycle" but "person at 2.1m, bicycle at 4.5m"
- **Object-centric spatial context** — each entity gets its position, depth, mask, and trajectory
- **Scene geometry** — free paths, obstacles, navigable corridors

### Layer 3 — Scene Graph

A core research contribution. Every frame produces a **metric scene graph** — a structured representation of spatial relationships:

```
Person_12 ──[1.8m, in_front_of]──► Bicycle_03
Person_12 ──[near]──────────────► TrafficCone_07
Bicycle_03 ──[left_of]──────────► Parked_Car_11
```

Relations include: `left_of`, `right_of`, `in_front_of`, `behind`, `near`, `overlapping`, `contains`

### Layer 4 — Memory

Unlike frame-based systems, CortexVision **never forgets**. Every tracked object accumulates a life history:

```
Person_12  →  Appeared (frame 1)
           →  Walking toward bicycle (frames 1–47)
           →  Reached bicycle (frame 48)
           →  Mounted bicycle (frames 48–61)
           →  Accelerating, heading NE (frames 62–...)
```

Four stores: Object Memory · Trajectory Store · Interaction Memory · History Buffer

### Layer 5 — World Model

A continuously-updated global state. All entities, all relations, all events — unified into one coherent world representation that predicts what happens next.

### Layer 6 — Navigation Intelligence

Transforms scene understanding into actionable spatial intelligence:

- **Bird's-Eye View projection** — top-down spatial map from monocular video
- **Occupancy grid** — per-cell passability scores
- **Free-path detection** — navigable corridors computed in real time
- **Path planning** — safe route generation for robotics and assistive systems

### Layer 7 — Reasoning

The top of the stack. A VLM (vision-language model) receives the full world state and reasons over it:

- Why did event X happen?
- What is entity Y likely to do next?
- Is there a collision risk between A and B?
- What changed between T=0 and T=now?

---

## Core Research Contributions

| ID | Contribution | What it solves |
|---|---|---|
| **C1** | Depth-Aware Object Fusion | Object-centric 3D reasoning from monocular video |
| **C2** | Metric Scene Graph Generation | Spatially grounded relationships — not just labels |
| **C3** | Persistent Object Memory | Long-term state tracking across arbitrary time horizons |
| **C4** | Temporal Scene Graph Evolution | How relationships *change* over time |
| **C5** | Predictive World Modeling | Future event forecasting from observed patterns |
| **C6** | Navigation-Oriented Scene Understanding | Scene representations designed for path planning |

---

## Research Question

> *Can a machine construct and maintain a temporally consistent world model from monocular video streams using multimodal perception, scene graphs, memory, and predictive reasoning?*

This framework is the attempt to answer that question — built from scratch, one component at a time.

---

## Repository Structure

```
CortexVision/
│
├── app/               ← Inference & demo entry points
├── benchmarks/        ← Evaluation harness & baselines
├── checkpoints/       ← Model weights (not tracked)
├── configs/           ← YAML configs for each component
├── core/              ← Fusion, scene graph, memory, world model
├── datasets/          ← Dataset loaders & preprocessing
├── docs/              ← Architecture docs & diagrams
├── evaluation/        ← Metrics: tracking, depth, scene graph quality
├── experiments/       ← Run logs & ablation results
├── models/            ← Model wrappers (YOLO, SAM2, Depth Pro, etc.)
├── notebooks/         ← Analysis & visualization notebooks
├── outputs/           ← Inference outputs (not tracked)
├── paper/             ← Draft writeup & figures
├── scripts/           ← Training, inference, export scripts
├── tests/             ← Unit tests per module
├── tools/             ← Visualization & debugging tools
└── utils/             ← Shared utilities
```

---

## Tech Stack

```
Perception    →   YOLO-World · Depth Pro · SAM2 · ByteTrack · RTMPose
Deep Learning →   PyTorch · OpenCV · NumPy
Reasoning     →   Hugging Face Transformers (VLM integration)
Visualization →   Streamlit · Matplotlib · OpenCV
Language      →   Python 3.10+
```

---

## Related Work

This project sits at the intersection of:

- **World models** — maintaining internal representations of dynamic environments
- **Scene graph generation** — structured relational representations of visual scenes
- **Monocular depth estimation** — inferring 3D structure from 2D video
- **Multi-object tracking** — persistent identity assignment across frames
- **Embodied AI** — perception systems designed to act, not just observe

---

## Status

This is active research — not a polished library. Components are being built, tested, and ablated iteratively.

- [x] Perception pipeline (YOLO + Depth Pro + SAM2 + ByteTrack)
- [x] Depth fusion layer
- [x] Metric scene graph generation
- [x] Object memory store
- [x] Trajectory tracking
- [ ] Temporal scene graph evolution (in progress)
- [ ] World model entity store (in progress)
- [ ] VLM reasoning integration
- [ ] Navigation layer (planned)
- [ ] Full evaluation suite (planned)

---

## Author

**Parth Tomar** — B.Tech. CSE, IIT Patna

[GitHub](https://github.com/couder-04) · [Email](mailto:parth04pt@gmail.com) · [LinkedIn](https://linkedin.com/in/parth-tomar)

---

<div align="center">

*Built with curiosity. Designed for worlds that don't stand still.*

</div>
```