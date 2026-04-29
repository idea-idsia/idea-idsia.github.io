---
layout: project
published: true

project_name: GINNGER
status: active
start: 2023
end:

short_summary: >
    Building an e-mobility optimal planning tool that identifies the optimal layout of EV charging infrastructure.

cover_image: ../assets/images/projects/ginnger.jpg

website:
code_repository:
project_coordinator: Fundación CIRCE

funding: Horizon Europe — HORIZON-CL5-2022-D4-02-02
aramis_url:

plotly: false

keywords:
    - Mixed-Integer Linear Programming
    - Optimisation
    - Neighbourhood Regeneration

contributors:
    - Matteo Salani, Vincenzo Giuffrida

partners:
    - SUPSI
    - Azienda Elettrica di Massagno (AEM)
    - Hive Power
---

## Overview

**GINNGER** is an Horizon Europe Innovation Action that supports the regeneration of European neighbourhoods through co-creation processes that engage heterogeneous stakeholder structures. The project combines social-science innovation with a digital toolkit of **13 digital solutions** organised in four blocks: Energy, Renovation, Resources, and Mobility; and validates them across **6 pilot sites** in 5 EU member states: Langreo (ES), Plovdiv (BG), Massagno (CH), Murcia (ES), Orte (IT), and Paris (FR).

![E-mobility Optimal Planning Tool ](/assets/images/projects/ginnger_overview.jpg){: width="400"}

IDeA's contribution focuses on the **Mobility block**, and specifically on **DS13 — E-mobility Optimal Planning Tool**, deployed in the Swiss pilot.

## IDeA's role

IDeA is involved in DS13, which consists of the implementation of an optimal **E-Mobility OPEM planning tool** using data-driven methods to identify the most opportune **locations** for the installation of **charging stations**.
The tool takes as input the local mobility patterns, the existing electrical and charging infrastructure, the candidate locations for new stations, and a portfolio of charger technologies, and returns an **investment plan** that balances **coverage of mobility demand** against capital **costs** and **grid-level constraints**.

![E-mobility Optimal Planning Tool ](/assets/images/projects/ginnger_graph.jpg){: width="800"}

The Swiss pilot covers the district of **Massagno**, a residential and mixed-use area. The district aims to **triple the penetration of public charging stations** within the neighbourhood as part of its regeneration strategy.

## Optimisation Approach

IDeA developed the **optimisation engine** for DS13. The problem is formulated as a **Mixed-Integer Linear Programme (MILP)** that decides:

- which **new stations** to open among a set of candidate sites.
- how many **chargers of each type** (e.g. slow, fast) to install at each station, including stations that already host some infrastructure.

The model accounts for several layers of real-world costs and constraints:

- **Capacity constraints** at each station, both in terms of total installed power and number of charging points, considering chargers already installed at existing sites.
- **Time-resolved power and demand balance** across the day. At every time interval the chargers installed at a station must be able to serve the energy and the number of EVs arriving from the routes assigned to it.
- **Budget constraint** that aggregates station opening costs, charger purchase costs, grid participation fees, electrical panel installation, civil engineering interventions.
- **Minimum utilisation** at every newly opened station, to avoid investing in infrastructure that would remain idle.

The model supports two configurable objectives that reflect different planning priorities:

| Objective    | Optimises for                                                                |
| ------------ | ---------------------------------------------------------------------------- |
| `coverage`   | Maximum coverage of mobility flows.                     |
| `kwh`        | Maximum energy delivered across served flows.     |
