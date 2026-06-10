---
layout: publication
title: "Distributed asynchronous column generation"
authors:
  - Saverio Basso
  - Alberto Ceselli
venue: "Computers & Operations Research"
year: 2022
type: journal
abstract: >
  We propose a revision of the classical column generation algorithm for solving Dantzig–Wolfe decompositions of mixed integer programs. It is meant to fully exploit the availability of distributed computing resources, making optimization algorithms in general purpose solvers to scale better.The main idea is to trigger massive parallelism by fully decoupling the computing flow of each component, including the resolution of the master problem, thus allowing different pricing algorithms to concurrently work on different sets of dual variables, and the master algorithm to asynchronously update dual information as soon as new columns are available.Our algorithms ensure the same optimality convergency properties of the classical method. Experiments on mixed integer programs for three benchmark problems from the combinatorial optimization literature prove our approach to be one order of magnitude faster than state-of-the-art general purpose solvers in computing high quality root node dual bounds. Even if devised to exploit clusters of machines which do not share memory space, our algorithms show to be faster than earlier attempts from the literature also when run on virtual machines hosted on a single physical one, proving this improvement to derive from our algorithmic methodology rather than technological factors.
pdf:
code:
arxiv:
doi: 10.1016/j.cor.2022.105894
tags:
  - Column Generation
  - Distributed Computing
  - Parallel computation
  - Asynchronous computation
  - Combinatorial Optimization
plotly: false
---

## BibTeX

```bibtex
@article{BASSO2022105894,
title = {Distributed asynchronous column generation},
journal = {Computers & Operations Research},
volume = {146},
pages = {105894},
year = {2022},
issn = {0305-0548},
doi = {https://doi.org/10.1016/j.cor.2022.105894},
author = {Saverio Basso and Alberto Ceselli},
keywords = {Dantzig–Wolfe decomposition, Column generation, Distributed computing}
}
```
