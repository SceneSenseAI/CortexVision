# SceneSenseAI — Research Paper Reference List
**Adaptive Multimodal Scene Understanding using VLM Fusion**
*Compiled: May 2026*

---

## Table of Contents

- [1. Object Detection — YOLO Family](#1-object-detection--yolo-family)
- [2. Object Tracking — ByteTrack](#2-object-tracking--bytetrack)
- [3. Depth Estimation](#3-depth-estimation)
- [4. Semantic Segmentation](#4-semantic-segmentation)
- [5. Pose Estimation](#5-pose-estimation)
- [6. Vision Language Models (VLMs)](#6-vision-language-models-vlms)
- [7. Foundational Papers](#7-foundational-papers)
- [8. Scene Understanding & Multimodal Fusion](#8-scene-understanding--multimodal-fusion)
- [Repositories](#repositories)
- [Quick Reference — arXiv IDs](#quick-reference--arxiv-ids)

---

## 1. Object Detection — YOLO Family

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [1] | **YOLOv1** — You Only Look Once: Unified, Real-Time Object Detection | Redmon, Divvala, Girshick, Farhadi | CVPR 2016 | [arXiv](https://arxiv.org/abs/1506.02640) · [PDF](https://arxiv.org/pdf/1506.02640) |
| [2] | **YOLOv4** — Optimal Speed and Accuracy of Object Detection | Bochkovskiy, Wang, Liao | 2020 | [arXiv](https://arxiv.org/abs/2004.10934) · [PDF](https://arxiv.org/pdf/2004.10934) |
| [3] | **YOLOv8** — Real-Time Flying Object Detection with YOLOv8 | Reis, Kupec, Hong, Daoudi | 2023 | [arXiv](https://arxiv.org/abs/2305.09972) · [PDF](https://arxiv.org/pdf/2305.09972) |
| [4] | **YOLOv8 (IEEE)** — A Novel Object Detection Algorithm with Enhanced Performance and Robustness | — | IEEE 2024 | [IEEE Xplore](https://ieeexplore.ieee.org/document/10533619/) |
| [5] | **YOLO Decade Survey** — A Decade of You Only Look Once (YOLO) for Object Detection | — | 2025 | [arXiv](https://arxiv.org/abs/2504.18586) |

---

## 2. Object Tracking — ByteTrack

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [6] | **ByteTrack** — Multi-Object Tracking by Associating Every Detection Box | Zhang, Sun, Jiang et al. | ECCV 2022 | [arXiv](https://arxiv.org/abs/2110.06864) · [PDF](https://arxiv.org/pdf/2110.06864) · [GitHub](https://github.com/FoundationVision/ByteTrack) |

---

## 3. Depth Estimation

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [7] | **MiDaS** — Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-shot Cross-dataset Transfer | Ranftl, Lasinger, Hafner, Schindler, Koltun | TPAMI 2020 | [arXiv](https://arxiv.org/abs/1907.01341) · [PDF](https://arxiv.org/pdf/1907.01341) · [GitHub](https://github.com/isl-org/MiDaS) |
| [8] | **DPT** — Vision Transformers for Dense Prediction | Ranftl, Bochkovskiy, Koltun | ICCV 2021 | [arXiv](https://arxiv.org/abs/2103.13413) · [PDF](https://arxiv.org/pdf/2103.13413) · [CVF](https://openaccess.thecvf.com/content/ICCV2021/html/Ranftl_Vision_Transformers_for_Dense_Prediction_ICCV_2021_paper.html) · [GitHub](https://github.com/isl-org/DPT) |
| [9] | **Depth Anything V1** — Unleashing the Power of Large-Scale Unlabeled Data | Yang, Kang, Huang, Xu, Feng, Zhao | CVPR 2024 | [arXiv](https://arxiv.org/abs/2401.10891) · [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Yang_Depth_Anything_Unleashing_the_Power_of_Large-Scale_Unlabeled_Data_CVPR_2024_paper.pdf) |
| [10] | **Depth Anything V2** | Yang, Kang, Huang, Zhao et al. | NeurIPS 2024 | [arXiv](https://arxiv.org/abs/2406.09414) · [PDF](https://arxiv.org/pdf/2406.09414) · [Project Page](https://depth-anything-v2.github.io/) |

---

## 4. Semantic Segmentation

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [11] | **SegFormer** — Simple and Efficient Design for Semantic Segmentation with Transformers | Xie, Wang, Yu, Anandkumar, Alvarez, Luo | NeurIPS 2021 | [arXiv](https://arxiv.org/abs/2105.15203) · [PDF](https://arxiv.org/pdf/2105.15203v2) · [NeurIPS](https://proceedings.neurips.cc/paper/2021/hash/64f1f27bf1b4ec22924fd0acb550c235-Abstract.html) · [GitHub](https://github.com/NVlabs/SegFormer) |
| [12] | **SAM** — Segment Anything | Kirillov, Mintun, Ravi, Mao et al. | ICCV 2023 | [arXiv](https://arxiv.org/abs/2304.02643) · [PDF](https://arxiv.org/pdf/2304.02643) · [GitHub](https://github.com/facebookresearch/segment-anything) |
| [13] | **Mask R-CNN** | He, Gkioxari, Dollár, Girshick | ICCV 2017 | [arXiv](https://arxiv.org/abs/1703.06870) · [PDF](https://arxiv.org/pdf/1703.06870) · [CVF](https://openaccess.thecvf.com/content_iccv_2017/html/He_Mask_R-CNN_ICCV_2017_paper.html) |
| [28] | **SAM 2** — Segment Anything in Images and Videos | Ravi et al. (Meta AI) | 2024 | [arXiv](https://arxiv.org/abs/2408.00714) |

---

## 5. Pose Estimation

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [14] | **OpenPose** — Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields | Cao, Hidalgo, Simon, Wei, Sheikh | TPAMI 2019 | [arXiv](https://arxiv.org/abs/1812.08008) · [PDF](https://arxiv.org/pdf/1812.08008) · [ACM/IEEE](https://dl.acm.org/doi/10.1109/TPAMI.2019.2929257) |
| [15] | **MediaPipe** — A Framework for Building Perception Pipelines | Lugaresi, Tang, Nash et al. | 2019 | [arXiv](https://arxiv.org/abs/1906.08172) |
| [16] | **BlazePose / MediaPipe Pose** — On-Device Real-Time Body Pose Tracking | — | 2020 | [arXiv](https://arxiv.org/abs/2006.10204) · [Blog](https://research.google/blog/on-device-real-time-body-pose-tracking-with-mediapipe-blazepose/) |
| [17] | **YOLOv8-Pose** *(part of YOLOv8 ecosystem)* | Ultralytics | — | [Docs](https://docs.ultralytics.com/tasks/pose/) · see also [3] |

---

## 6. Vision Language Models (VLMs)

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [18] | **BLIP-2** — Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models | Li, Li, Savarese, Hoi | ICML 2023 | [arXiv](https://arxiv.org/abs/2301.12597) · [PDF](https://arxiv.org/pdf/2301.12597) |
| [19] | **LLaVA** — Visual Instruction Tuning | Liu, Li, Wu, Lee | NeurIPS 2023 (Oral) | [arXiv](https://arxiv.org/abs/2304.08485) · [PDF](https://arxiv.org/pdf/2304.08485) · [GitHub](https://github.com/haotian-liu/LLaVA) |
| [20] | **Flamingo** — A Visual Language Model for Few-Shot Learning | Alayrac, Donahue, Luc, Miech et al. (DeepMind) | NeurIPS 2022 | [arXiv](https://arxiv.org/abs/2204.14198) · [PDF](https://arxiv.org/pdf/2204.14198) · [DeepMind PDF](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf) |
| [21] | **GPT-4 Technical Report** (GPT-4V) | OpenAI | 2023 | [arXiv](https://arxiv.org/abs/2303.08774) · [PDF](https://arxiv.org/pdf/2303.08774) · [Official](https://cdn.openai.com/papers/gpt-4.pdf) |
| [22] | **Qwen-VL** — A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond | Bai, Bai, Yang et al. (Alibaba) | 2023 | [arXiv](https://arxiv.org/abs/2308.12966) · [PDF](https://arxiv.org/pdf/2308.12966) · [GitHub](https://github.com/QwenLM/Qwen-VL) |
| [23] | **Qwen2-VL** — Enhancing Vision-Language Model's Perception of the World at Any Resolution | Wang, Bai et al. (Alibaba) | 2024 | [arXiv](https://arxiv.org/abs/2409.12191) · [PDF](https://arxiv.org/pdf/2409.12191) |
| [30] | **InstructBLIP** — Towards General-purpose Vision-Language Models with Instruction Tuning | Dai, Li et al. | NeurIPS 2023 | [arXiv](https://arxiv.org/abs/2305.06500) |
| [31] | **LLaVA-1.5** — Improved Baselines with Visual Instruction Tuning | Liu, Li, Li, Lee | 2023 | [arXiv](https://arxiv.org/abs/2310.03744) |

---

## 7. Foundational Papers

| # | Paper | Authors | Venue | Links |
|---|-------|---------|-------|-------|
| [24] | **Faster R-CNN** — Towards Real-Time Object Detection with Region Proposal Networks | Ren, He, Girshick, Sun | NIPS 2015 | [arXiv](https://arxiv.org/abs/1506.01497) |
| [25] | **CLIP** — Learning Transferable Visual Models From Natural Language Supervision | Radford, Kim et al. (OpenAI) | ICML 2021 | [arXiv](https://arxiv.org/abs/2103.00020) |
| [26] | **ViT** — An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale | Dosovitskiy, Beyer et al. | ICLR 2021 | [arXiv](https://arxiv.org/abs/2010.11929) |
| [27] | **Attention Is All You Need** (Transformer) | Vaswani, Shazeer et al. | NeurIPS 2017 | [arXiv](https://arxiv.org/abs/1706.03762) |
| [29] | **SSIM** — Image Quality Assessment: From Error Visibility to Structural Similarity | Wang, Bovik, Sheikh, Simoncelli | IEEE TIP 2004 | [IEEE](https://ieeexplore.ieee.org/document/1284395) |
| [32] | **Chain-of-Thought Prompting** — Elicits Reasoning in Large Language Models | Wei, Wang et al. (Google) | NeurIPS 2022 | [arXiv](https://arxiv.org/abs/2201.11903) |
| [33] | **TensorRT** — Efficient Inference on GPUs | NVIDIA | — | [Docs](https://docs.nvidia.com/deeplearning/tensorrt/developer-guide/index.html) |

---

## 8. Scene Understanding & Multimodal Fusion

| # | Paper | Links |
|---|-------|-------|
| [41] | **Video Understanding with Multimodal Foundation Models: A Survey** | [arXiv](https://arxiv.org/abs/2309.12963) |
| [42] | **Visual Grounding in Video for Unsupervised Word Translation** | [arXiv](https://arxiv.org/abs/1912.11455) |
| [43] | **Hallucination Augmented Contrastive Learning for Multimodal Large Language Models** | [arXiv](https://arxiv.org/abs/2312.06968) |
| [44] | **Evaluating Object Hallucination in Large Vision-Language Models** | [arXiv](https://arxiv.org/abs/2305.10355) |
| [45] | **On the Robustness of Large Multimodal Models Against Image Adversarial Attacks** | [arXiv](https://arxiv.org/abs/2312.03777) |

---

## Repositories

| Library | GitHub |
|---------|--------|
| ByteTrack | [FoundationVision/ByteTrack](https://github.com/FoundationVision/ByteTrack) |
| Segment Anything (SAM) | [facebookresearch/segment-anything](https://github.com/facebookresearch/segment-anything) |
| SegFormer | [NVlabs/SegFormer](https://github.com/NVlabs/SegFormer) |
| MiDaS | [isl-org/MiDaS](https://github.com/isl-org/MiDaS) |
| DPT | [isl-org/DPT](https://github.com/isl-org/DPT) |
| LLaVA | [haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA) |
| Qwen-VL | [QwenLM/Qwen-VL](https://github.com/QwenLM/Qwen-VL) |

---

## Quick Reference — arXiv IDs

| Model | arXiv ID |
|-------|----------|
| YOLOv1 | [1506.02640](https://arxiv.org/abs/1506.02640) |
| YOLOv4 | [2004.10934](https://arxiv.org/abs/2004.10934) |
| YOLOv8 | [2305.09972](https://arxiv.org/abs/2305.09972) |
| ByteTrack | [2110.06864](https://arxiv.org/abs/2110.06864) |
| MiDaS | [1907.01341](https://arxiv.org/abs/1907.01341) |
| DPT | [2103.13413](https://arxiv.org/abs/2103.13413) |
| Depth Anything V1 | [2401.10891](https://arxiv.org/abs/2401.10891) |
| Depth Anything V2 | [2406.09414](https://arxiv.org/abs/2406.09414) |
| SegFormer | [2105.15203](https://arxiv.org/abs/2105.15203) |
| SAM | [2304.02643](https://arxiv.org/abs/2304.02643) |
| SAM 2 | [2408.00714](https://arxiv.org/abs/2408.00714) |
| Mask R-CNN | [1703.06870](https://arxiv.org/abs/1703.06870) |
| OpenPose | [1812.08008](https://arxiv.org/abs/1812.08008) |
| MediaPipe | [1906.08172](https://arxiv.org/abs/1906.08172) |
| BLIP-2 | [2301.12597](https://arxiv.org/abs/2301.12597) |
| LLaVA | [2304.08485](https://arxiv.org/abs/2304.08485) |
| LLaVA-1.5 | [2310.03744](https://arxiv.org/abs/2310.03744) |
| Flamingo | [2204.14198](https://arxiv.org/abs/2204.14198) |
| GPT-4 Report | [2303.08774](https://arxiv.org/abs/2303.08774) |
| Qwen-VL | [2308.12966](https://arxiv.org/abs/2308.12966) |
| Qwen2-VL | [2409.12191](https://arxiv.org/abs/2409.12191) |
| CLIP | [2103.00020](https://arxiv.org/abs/2103.00020) |
| ViT | [2010.11929](https://arxiv.org/abs/2010.11929) |
| Transformer | [1706.03762](https://arxiv.org/abs/1706.03762) |
| InstructBLIP | [2305.06500](https://arxiv.org/abs/2305.06500) |
| Chain-of-Thought | [2201.11903](https://arxiv.org/abs/2201.11903) |
| Faster R-CNN | [1506.01497](https://arxiv.org/abs/1506.01497) |

---

*All links verified as of May 2026. arXiv links follow the format `https://arxiv.org/abs/<ID>`.*
