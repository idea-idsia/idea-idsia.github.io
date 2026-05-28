---
layout: software
title: ANT-AI
published: true

project_name: "ANT-AI – Lightweight Framework for Multi-Agent AI Systems"
status: active

short_summary: >
  ANT-AI makes it easy to design, deploy, and experiment with multi-agent AI systems —
  from a single tool-driven agent to a full colony of collaborating peers communicating
  via the A2A protocol, on top of an LLM-agnostic core.

image: /assets/images/software/ant_ai.png
website: https://idea-idsia.github.io/ant-ai/
code_repository: https://github.com/idea-idsia/ant-ai

plotly: false

keywords:
  - Multi-Agent Systems
  - AI Agents
  - Python
  - LLM
  - Workflow Automation
  - Open Source

contributors:
  - Cezar Sas
  - Vincenzo Giuffrida
  - Sandra Mitrović
  - Matteo Salani
---

## Overview

**ANT-AI** is a Python framework for building multi-agent AI systems — from a single tool-driven agent to a coordinated colony of collaborating peers — designed to be easy to pick up whether you are running research experiments or integrating autonomous agents into a real application.

Built around a graph-based workflow engine and native A2A (Agent-to-Agent) communication, agents delegate tasks to one another without any custom glue code. The LLM-agnostic core means you can swap models or providers at any point without touching agent logic, keeping experiments reproducible and production deployments flexible.

ANT-AI exposes exactly what runs, when, and why — giving researchers the transparency they need to publish and practitioners the control they need to ship.

Key capabilities include:

- **Graph-based workflow orchestration** for structured, auditable agent pipelines
- **Native A2A communication** for agent-to-agent delegation and multi-agent collaboration
- **MCP tool integration** with a built-in registry and support for custom tools
- **Memory backends** including Mem0 integration for persistent agent state across interactions
- **Built-in observability** via Langfuse tracing and lifecycle hooks for guardrails and monitoring

ANT-AI is available on PyPI (requires Python 3.14+):

```bash
uv add ant-ai
```
