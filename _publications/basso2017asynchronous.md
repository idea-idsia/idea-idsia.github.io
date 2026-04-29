---
layout: publication
title: "Asynchronous Column Generation"
authors:
  - Saverio Basso
  - Alberto Ceselli
venue: "Proceedings of the 19th Workshop on Algorithm Engineering and Experiments (ALENEX)"
year: 2017
type: conference
abstract: >
  In this paper we face a very fundamental problem in Operations Research: to find good dual bounds to generic mixed integer mathematical programs (MIPs) as quickly as possible. In particular, we focus on the scenario where large scale data needs to be considered, multicore CPU architectures are available, and massive parallelism can be exploited by means of decomposition methods. We consider column generation techniques to solve extended formulations obtained by means of Dantzig-Wolfe decomposition for MIPs. We propose a concurrent algorithm, that relaxes the synchronized behavior of classical column generation. Our approach relies on simple data structures and efficient synchronization, still providing the same global convergence properties of classical sequential column generation methods. We present and discuss the results of an extensive experimental campaign, comparing our concurrent algorithm to both a naive parallelization of column generation and the cutting planes algorithm implemented in state-of-the-art commercial optimization packages, considering large scale datasets of a hard packing problem from the literature as representative benchmark. Our approach turns out to be on average one order of magnitude faster than competitors, attaining almost linear speedups as the number of available CPU cores increases.
pdf:
code:
arxiv:
doi: 10.1137/1.9781611974768.16
tags:
  - Column Generation
  - Parallel computation
  - Asynchronous computation
  - Algorithm Engineering
  - Combinatorial Optimization
plotly: false
---

## BibTeX

```bibtex
@inbook{doi:10.1137/1.9781611974768.16,
author = {S. Basso and A. Ceselli},
title = {Asynchronous Column Generation},
booktitle = {2017 Proceedings of the Meeting on Algorithm Engineering and Experiments (ALENEX)},
chapter = {},
pages = {197-206},
doi = {10.1137/1.9781611974768.16},
URL = {https://epubs.siam.org/doi/abs/10.1137/1.9781611974768.16},
eprint = {https://epubs.siam.org/doi/pdf/10.1137/1.9781611974768.16}
}
```
