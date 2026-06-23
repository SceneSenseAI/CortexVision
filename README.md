<div align="center">

<br/>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=13&duration=3000&pause=1000&color=6C63FF&center=true&vCenter=true&width=600&lines=Persistent+World+Modeling+%C2%B7+Scene+Understanding;Depth+Fusion+%C2%B7+Scene+Graphs+%C2%B7+Predictive+Reasoning;Not+detection.+Not+captioning.+World+modeling." alt="Typing SVG" />

<br/><br/>

# 🌍 CortexVision

### *A machine that doesn't just see — it remembers, reasons, and predicts.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)

[![Status](https://img.shields.io/badge/Status-Active%20Research-brightgreen?style=flat-square)]()
[![IIT Patna](https://img.shields.io/badge/IIT%20Patna-Computer%20Science-7B2FBE?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

<br/>

</div>

---

<div align="center">

## The Problem with Modern Computer Vision

</div>

Every major vision system today is stateless. It sees a frame. It outputs boxes. It forgets.

```
                    ┌──────────────────────────────────────────┐
  Frame t=0  ──────►│  Detector  │──► [person, bicycle, car]  │
  Frame t=1  ──────►│  Detector  │──► [person, bicycle, car]  │  ← no memory
  Frame t=2  ──────►│  Detector  │──► [person, bicycle, car]  │  ← no context
                    └──────────────────────────────────────────┘
```

No depth. No identity. No relationships. No history. No prediction.

**CortexVision is built to fix that.**

---

<div align="center">

## What CortexVision Does

</div>

```
  Video Stream
       │
       ▼
  ┌───────────────────────────────────────────────────────────┐
  │  PERCEPTION     YOLO-World · Depth Pro · SAM2             │
  │                 ByteTrack · RTMPose                        │
  ├───────────────────────────────────────────────────────────┤
  │  FUSION         Detection + Depth + Segmentation          │
  │                 → Metric 3D object positions              │
  ├───────────────────────────────────────────────────────────┤
  │  SCENE GRAPH    Spatial relations between all entities    │
  │                 left_of · behind · near · overlapping     │
  ├───────────────────────────────────────────────────────────┤
  │  MEMORY         Every object. Every interaction.          │
  │                 Full trajectory history.                  │
  ├───────────────────────────────────────────────────────────┤
  │  WORLD MODEL    Global state. Event engine. Predictions.  │
  ├───────────────────────────────────────────────────────────┤
  │  NAVIGATION     BEV · Occupancy Grid · Path Planning      │
  ├───────────────────────────────────────────────────────────┤
  │  REASONING      VLM over world state. Future prediction.  │
  └───────────────────────────────────────────────────────────┘
       │
       ▼
  Structured world understanding — not just bounding boxes
```

---

<div align="center">

## Core Research Question

</div>

> **Can a machine construct and maintain a temporally consistent world model from monocular video streams using multimodal perception, scene graphs, memory, and predictive reasoning?**

Traditional vision systems answer: *What objects exist?*

CortexVision answers: *What exists, where is it, how is it changing, what is it interacting with, and what will happen next?*

---

<div align="center">

## System Architecture — Deep Dive

</div>

### 🔍 Layer 1 · Perception

Five models run in parallel on every frame:

| Model | Task | Output |
|---|---|---|
| **YOLO-World** | Open-vocabulary detection | Bounding boxes for *any* object class |
| **Grounding DINO** | Language-conditioned detection | Text-prompted localization |
| **Depth Pro** | Metric monocular depth | Per-pixel real-world distances (meters) |
| **SAM2** | Video segmentation | Per-object pixel masks across frames |
| **ByteTrack** | Multi-object tracking | Persistent IDs across 500+ frames |
| **RTMPose** | Human pose estimation | Body keypoints for action understanding |

---

### ⚡ Layer 2 · Fusion

The first research challenge: fusing three imperfect signals into one coherent 3D representation.

```
  Detection   ──┐
                ├──► Depth-Aware Fusion ──► Object @ (x, y, z) meters
  Depth       ──┤
                │    "Person_12 is 2.1m away, slightly left of center"
  Segmentation ─┘    "Bicycle_03 is 4.5m away, directly ahead"
```

Not *"person is closer than bicycle"* — actual metric positions in 3D space.

**Components:**
- `Detection Fusion` — associates depth map regions with detected bounding boxes
- `Depth Fusion` — lifts 2D boxes into metric 3D coordinates
- `Object Association` — links detections across models into unified entity representations
- `Scene Builder` — assembles all entities into a coherent frame-level scene

---

### 🕸️ Layer 3 · Scene Graph

A core research contribution. Every frame produces a **metric scene graph** — not just what exists, but the structured spatial relationships between everything.

```
  Person_12  ──[1.8m · in_front_of]──► Bicycle_03
  Person_12  ──[0.4m · near]──────────► TrafficCone_07
  Bicycle_03 ──[left_of]──────────────► ParkedCar_11
  ParkedCar_11 ──[contains]───────────► Passenger_05
```

**Supported relations:**
```
  left_of    right_of    in_front_of    behind
  near       overlapping    contains    approaching
```

The graph is serialized and stored — queryable at any point in time.

---

### 🧠 Layer 4 · Memory

Unlike any frame-based system, CortexVision **never forgets**.

Every tracked entity gets a persistent memory record:

```
  Person_12
  ──────────────────────────────────────────────────
  frame   1  │  Appeared at (2.3m, left-center)
  frame  12  │  Walking east at ~1.2 m/s
  frame  31  │  Slowing — approaching Bicycle_03
  frame  48  │  Reached Bicycle_03
  frame  61  │  Mounted bicycle
  frame  62+ │  Accelerating northeast
```

**Four memory stores:**

| Store | What it tracks |
|---|---|
| `Object Memory` | State history of every entity |
| `Trajectory Store` | Full position + velocity timelines |
| `Interaction Memory` | Every recorded entity-entity interaction |
| `History Buffer` | Raw frame-level scene snapshots |

---

### 🌐 Layer 5 · World Model

All memory, all entities, all events — unified into a single coherent world state.

```
  Entity Store     ── all known objects + current states
  World State      ── global snapshot at time T
  Event Engine     ── detects and logs semantic events
                      ("Person mounted bicycle", "Vehicle stopped")
  Future Predictor ── forecasts likely next states
```

---

### 🗺️ Layer 6 · Navigation Intelligence

Transforms the world model into spatial representations for robotics and assistive systems.

- **BEV Projection** — Bird's-Eye View: top-down 2D map from monocular video
- **Occupancy Grid** — per-cell passability scores across the scene
- **Corridor Detection** — free navigable paths identified in real time
- **Path Planning** — safe route generation accounting for dynamic obstacles

---

### 💬 Layer 7 · Reasoning

The top of the stack. A VLM receives the full world state and reasons over it in natural language.

```
  Input:   World state @ T=247 + event history + future predictor output

  Output:  "Person_12 has been stationary for 4 seconds near an obstacle.
            Based on trajectory, they are likely preparing to cross.
            Collision risk with Vehicle_03 is elevated — 73% probability
            of path intersection within 6 seconds."
```

**Reasoning capabilities:**
- `Temporal Understanding` — what changed and when
- `VLM Reasoning` — natural language queries over the world state
- `Event Explanation` — *why* did this happen?
- `Future Prediction` — what happens next?

---

<div align="center">

## Research Contributions

</div>

| ID | Title | Description |
|---|---|---|
| **C1** | Depth-Aware Object Fusion | Lifting 2D detections into metric 3D using monocular depth |
| **C2** | Metric Scene Graph Generation | Spatially-grounded relational graphs with real-world distances |
| **C3** | Persistent Object Memory | Long-horizon state tracking with full interaction history |
| **C4** | Temporal Scene Graph Evolution | Tracking how spatial relationships change over time |
| **C5** | Predictive World Modeling | Forecasting future interactions from observed patterns |
| **C6** | Navigation-Oriented Scene Understanding | Perception representations designed for path planning |

---

<div align="center">

## Key Capabilities

</div>

<table>
<tr>
<td width="50%">

**🎯 Open-Vocabulary Detection**

Detect any object — not just fixed label sets.

```
person          bicycle
helmet          wheelchair
traffic cone    construction barrier
```
Models: YOLO-World, Grounding DINO

</td>
<td width="50%">

**📏 Metric Depth Estimation**

Real distances. Not relative rankings.

```
Person_12  →  2.1m
Bicycle_03 →  4.5m
Vehicle_07 →  9.2m
```
Model: Depth Pro

</td>
</tr>
<tr>
<td width="50%">

**🔲 Precise Segmentation**

Pixel-level object boundaries.

```
outputs:
  - per-object masks
  - free-space regions
  - scene structure map
```
Model: SAM2

</td>
<td width="50%">

**🔗 Persistent Tracking**

Same identity. Hundreds of frames.

```
Frame   1  →  Person #12
Frame  50  →  Person #12
Frame 500  →  Person #12
```
Model: ByteTrack

</td>
</tr>
<tr>
<td width="50%">

**⏳ Temporal Scene Graphs**

Relationships that evolve:

```
Person near bicycle
       ↓
Person touching bicycle
       ↓
Person riding bicycle
```

</td>
<td width="50%">

**🔮 Future Event Prediction**

What happens next:

```
→ crossing road
→ approaching obstacle
→ entering corridor
→ possible collision
```

</td>
</tr>
</table>

---

<div align="center">

## Repository Structure

</div>

```
CortexVision/
│
├── 📱 app/               ← Demo entry points & inference scripts
├── 📊 benchmarks/        ← Evaluation harness & baseline comparisons
├── 🗃️  checkpoints/       ← Model weights (gitignored)
├── ⚙️  configs/           ← YAML configs for every component
├── 🧠 core/              ← Fusion, scene graph, memory, world model
├── 📦 datasets/          ← Loaders & preprocessing pipelines
├── 📚 docs/              ← Architecture docs, diagrams, writeups
├── 📈 evaluation/        ← Metrics: depth, tracking, scene graph quality
├── 🧪 experiments/       ← Run logs, ablations, result snapshots
├── 🤖 models/            ← Wrappers: YOLO, SAM2, Depth Pro, ByteTrack
├── 📓 notebooks/         ← Analysis & visualization notebooks
├── 🖼️  outputs/           ← Inference outputs (gitignored)
├── 📄 paper/             ← Draft writeup & figures
├── 🚀 scripts/           ← Training, inference, export utilities
├── ✅ tests/             ← Unit tests per module
├── 🛠️  tools/             ← Visualization & debugging helpers
└── 🔧 utils/             ← Shared utilities & helpers
```

---

<div align="center">

## Tech Stack

</div>

```
┌──────────────┬──────────────────────────────────────────────────────┐
│ Perception   │ YOLO-World · Grounding DINO · Depth Pro              │
│              │ SAM2 · ByteTrack · RTMPose                           │
├──────────────┼──────────────────────────────────────────────────────┤
│ Deep Learning│ PyTorch 2.0+ · torchvision · CUDA                    │
├──────────────┼──────────────────────────────────────────────────────┤
│ Vision       │ OpenCV · Pillow · scikit-image                       │
├──────────────┼──────────────────────────────────────────────────────┤
│ Data         │ NumPy · Pandas · NetworkX (scene graphs)             │
├──────────────┼──────────────────────────────────────────────────────┤
│ Reasoning    │ Hugging Face Transformers (VLM integration)          │
├──────────────┼──────────────────────────────────────────────────────┤
│ Visualization│ Streamlit · Matplotlib · Gradio                      │
├──────────────┼──────────────────────────────────────────────────────┤
│ Language     │ Python 3.10+                                          │
└──────────────┴──────────────────────────────────────────────────────┘
```

---

<div align="center">

## Research Context

</div>

CortexVision sits at the intersection of five active research areas:

| Area | Relevance |
|---|---|
| **World Models** | Maintaining internal representations of dynamic environments |
| **Scene Graph Generation** | Structured relational understanding of visual scenes |
| **Monocular Depth Estimation** | Inferring 3D structure from 2D video — no LiDAR required |
| **Multi-Object Tracking** | Persistent identity across long temporal horizons |
| **Embodied AI** | Perception systems designed to act, not just observe |

---

<div align="center">

## Progress

</div>

> Active research — not a polished library. Components built, tested, and ablated iteratively.

**Perception & Core**
- [x] Multi-model perception pipeline (YOLO-World + Depth Pro + SAM2 + ByteTrack)
- [x] Metric depth fusion layer
- [x] Per-object 3D position estimation
- [x] Object memory store
- [x] Trajectory tracking & storage
- [x] Metric scene graph generation

**World Modeling**
- [ ] Temporal scene graph evolution *(in progress)*
- [ ] World model entity store *(in progress)*
- [ ] Event engine & semantic event detection *(planned)*
- [ ] Future predictor module *(planned)*

**Reasoning & Navigation**
- [ ] VLM reasoning integration *(planned)*
- [ ] BEV projection & occupancy grid *(planned)*
- [ ] Path planning layer *(planned)*
- [ ] Full evaluation suite *(planned)*

---

<div align="center">

## Author

<br/>

**Parth Tomar**
B.Tech. Computer Science & Engineering · IIT Patna

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-couder--04-181717?style=for-the-badge&logo=github)](https://github.com/couder-04)
[![Email](https://img.shields.io/badge/Email-parth04pt%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:parth04pt@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-parth--tomar-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/parth-tomar)

<br/>

---

*Built with curiosity. Designed for worlds that don't stand still.*

<br/>

</div>
