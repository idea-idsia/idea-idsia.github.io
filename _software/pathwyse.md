---
layout: software
title: PathWyse
project_name: PathWyse
status: active
start: 2021
end:
short_summary:
  A C++ and Python framework to model and solve Resource Constrained Shortest Path Problems.
   
image: /assets/images/software/pathwyse.png     
website: https://github.com/pathwyse/pathwyse 
project_coordinator: Matteo Salani

keywords:
  - Shortest Path Problems
  - Dynamic Programming
  - Column Generation
  - Machine learning
  - Solver

contributors:
  - Saverio Basso
  - Alessandro Minoli
  - Matteo Salani

funding: 
plotly: false

partners:

---

## Overview


PathWyse is a project designed to address Resource Constrained Shortest Path Problems (RCSPP), combining state-of-the-art exact algorithms with a modular architecture for rapid experimentation and integration. It is particularly suited for problems arising as pricing subproblems in column generation, as well as routing and scheduling applications with multiple constraints. 

The library can be used both as a high-performance C++ solver for real-world applications and as a research platform for developing and testing new algorithmic ideas.

Pathwyse provides an interactive mode in Python, along with Python interfaces for flexible usage.

PathWyse is available under a dual licensing model: an open-source license and a commercial license.


**_For Industries_**:

PathWyse can be used as a high-performance solver for constrained shortest path problems. It can be executed from the command line, embedded in C++ applications, or accessed through a Python interface.

PathWyse provides practitioners with fast, reliable exact solutions to complex constrained shortest path problems, helping to reduce planning time, resource utilization, and, in general, support decision-making in real-world transportation, logistic and scheduling tasks. Typical applications also include solving pricing subproblems in column generation for vehicle routing, crew rostering, path-based scheduling and many other problems.

The library includes configuration files for controlling algorithmic behavior and collecting performance data, so it can be integrated into larger pipelines without modifying the source code.



**_For Academia_**: 

PathWyse is also designed as a research-oriented framework where algorithmic components are explicit and configurable. The goal is to allow experimentation without reimplementing the full machinery behind labeling algorithms.

The library provides implementations of bidirectional dynamic programming, DSSR and NG-path relaxations, and their hybridizations, together with mechanisms for label candidate selection, dominance, and join procedures.

Its internal structure is modular: resources, labels, and extension functions can be customized, and new algorithmic variants can be introduced without modifying the entire codebase. This makes the library suitable for studying new problems, designing dominance rules and relaxation schemes, or formulating pricing subproblems in column generation.

## Supported Problems and Techniques

PathWyse provides support for:

- RCSPPs with one or more monotone resources;
- Acyclic networks and elementary cyclic variants through relaxation schemes;
- Capacity, time, node limits, and time windows built-in resources;
- Custom resource types through the `Resource` class.
- Routing, scheduling, and pricing subproblems in column generation.


The library includes the following techniques and features.

- **Bi-directional search:** Dynamic programming labeling algorithms are implemented in both mono-directional and bi-directional [Righini and Salani, 2006] fashion;
- **Relaxation schemes:** Decremental State Space Relaxation (DSSR) [Righini and Salani, 2008], NG-path relaxations (NG) [Baldacci et al., 2011] and hybridizations [Martinelli et al., 2014] are included to tackle the Elementary RCSPP;
- **Dynamic half-way point:** The budget of the critical resource is automatically adjusted in bidirectional algorithms, similarly to [Sadykov et al., 2020]
- **Candidate and join strategies:** multiple methods for selecting candidates and performing join operations in labeling algorithms.
- **A\*-based algorithm:** a custom implementation of the A* algorithm proposed by [Ahmadi et al. 2021] is provided for single resource acyclic problems;

PathWyse also supports simple heuristics, and features data collection tools.


## Publications

The library is described in the following paper: [https://doi.org/10.1080/10556788.2023.2296978](https://doi.org/10.1080/10556788.2023.2296978)
