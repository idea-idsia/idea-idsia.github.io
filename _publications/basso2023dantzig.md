---
layout: publication
title: "A data driven Dantzig–Wolfe decomposition framework"
authors:
  - Saverio Basso
  - Alberto Ceselli
venue: "Mathematical Programming Computation"
year: 2023
type: journal
abstract: >
  We face the issue of finding alternative paradigms for the resolution of generic Mixed Integer Programs (MIP), by considering the perspective option of general purpose solvers which switch to decomposition methods when pertinent. Currently, the main blocking factor in their design is the problem of automatic decomposition of MIPs, that is to produce good MIP decompositions algorithmically, looking only at the algebraic structure of the MIP instance. We propose to employ Dantzig–Wolfe reformulation and machine learning methods to obtain a fully data driven automatic decomposition framework. We also design strategies and introduce algorithmic techniques in order to make such a framework computationally effective. An extensive experimental analysis shows our framework to grant substantial improvements, in terms of both solutions quality and computing time, with respect to state-of-the-art automatic decomposition techniques. It also allows us to gain insights into the relative impact of different techniques. As a side product of our research, we provide a dataset of more than 31 thousand random decompositions of MIPLIB instances, with 121 features, including computations of their root node relaxation.
pdf:
code:
arxiv:
doi: 10.1007/s12532-022-00230-4
tags:
  - Combinatorial Optimization
  - Machine Learning
  - Mixed Integer Programming
  - Decomposition
plotly: false
---

## BibTeX

```bibtex
@article{basso2023dantzig,
  title   = {A data driven {Dantzig}--{Wolfe} decomposition framework},
  author  = {Basso, Saverio and Ceselli, Alberto},
  journal = {Mathematical Programming Computation},
  volume  = {15},
  number  = {1},
  pages   = {153-194},
  year    = {2023},
  doi     = {10.1007/s12532-022-00230-4}
}
```
