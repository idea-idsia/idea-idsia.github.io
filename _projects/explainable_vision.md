---
layout: project
project_name: Explainable Vision Systems
status: active
start: 2023
end:
short_summary: >
  Building computer vision models whose decisions can be explained to
  non-expert users through natural language and visual highlights.
cover_image:        # /assets/images/projects/explainable_vision.jpg
website:
code_repository:
project_coordinator:
funding: EU Horizon Europe
aramis_url:
plotly: false
keywords:
  - Computer Vision
  - Explainable AI
  - Deep Learning
contributors:
  - Anna Rossi
  - John Smith
partners:
---

## Overview

This project investigates how deep neural networks for vision can be made **interpretable without sacrificing accuracy**. We develop post-hoc explanation methods and inherently interpretable architectures that generate natural language rationales alongside visual saliency maps.

## Pipeline

```mermaid
graph TD
    I[Input Image] --> BB[Backbone CNN / ViT]
    BB --> F[Feature Maps]
    F --> CLS[Classifier Head]
    F --> EXP[Explanation Module]
    CLS --> PRED[Prediction]
    EXP --> SAL[Saliency Map]
    EXP --> NL[Natural Language Rationale]
    PRED --> OUT[Final Output]
    SAL --> OUT
    NL --> OUT
```

## Methods

### Saliency-Based Explanations

We extend gradient-based attribution methods (GradCAM, Integrated Gradients) to produce **faithful** attributions — explanations that accurately reflect the model's reasoning rather than human-plausible post-hoc rationalisations.

### Natural Language Rationales

A lightweight language decoder is jointly trained to output a sentence explaining the classification decision. We use contrastive supervision to ensure the rationale is grounded in the visual evidence.

### User Studies

Explanations are evaluated not only by automated faithfulness metrics but through **user studies** with domain experts and lay users, measuring how well explanations support correct mental models of the model's behaviour.

## Evaluation

| Method | Faithfulness ↑ | User Trust ↑ | Accuracy |
|--------|---------------|--------------|----------|
| GradCAM baseline | 0.61 | 3.2 / 5 | 91.4% |
| Our saliency | 0.79 | 3.8 / 5 | 91.2% |
| Our saliency + NL | 0.79 | 4.4 / 5 | 90.9% |

## Publications

- Rossi, A., Smith, J. (2024). *Faithful Visual Explanations with Language Grounding*. CVPR 2024.
