---
layout: project
project_name: Emergent Communication in Multi-Agent Systems
status: completed
start: 2020
end: 2023
short_summary: >
  Studied how communication protocols emerge spontaneously among cooperative
  agents trained with multi-agent reinforcement learning.
cover_image:        # /assets/images/projects/multiagent_comm.jpg
website:
code_repository:
project_coordinator:
funding: Internal Research Fund
aramis_url:
plotly: false
keywords:
  - Multi-Agent Systems
  - Game Theory
  - Reinforcement Learning
contributors:
  - Jane Doe
partners:
---

## Overview

This project investigated **emergent communication** — the spontaneous development of shared symbolic languages among agents that are trained only with task reward, with no pre-specified communication protocol. We studied the conditions under which grounded, compositional languages arise and how they relate to natural language structure.

## Communication Protocol

```mermaid
sequenceDiagram
    participant A1 as Agent 1 (Sender)
    participant CH as Channel
    participant A2 as Agent 2 (Receiver)
    A1->>A1: Observe environment
    A1->>CH: Emit discrete symbol sequence
    CH->>A2: Deliver message
    A2->>A2: Decode + act
    A2-->>A1: Shared reward signal
    Note over A1,A2: Repeat until protocol converges
```

## Key Findings

- Agents reliably develop consistent symbol-to-concept mappings when the referential game is sufficiently complex
- **Compositionality** (combining known symbols for novel concepts) emerges under population training but not in two-agent settings
- Emergent languages show topographic similarity to natural language when agents are trained with memory-limited architectures

## Evaluation Metrics

| Setting | Task Success ↑ | Compositionality (TRE) ↑ | Symbol Reuse ↑ |
|---------|---------------|--------------------------|----------------|
| 2-agent | 94% | 0.31 | Low |
| Population (10) | 91% | 0.67 | High |
| Population + bottleneck | 89% | 0.74 | High |

## Publications

- Doe, J. (2023). *Population Training Drives Compositional Emergence in Multi-Agent Communication*. ICLR 2023.
