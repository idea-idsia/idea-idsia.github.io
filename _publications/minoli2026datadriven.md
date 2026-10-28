---
layout: publication
title: "Data-Driven Dynamic Programming for Constrained Shortest Paths"
authors:
    - Alessandro Minoli
    - Saverio Basso
    - Matteo Salani
venue: SSRN
year: 2026
type: preprint
abstract: >
    The most successful approaches for solving the Elementary Resource Constrained Shortest Path Problem (ERCSPP) to optimality are based on Dynamic Programming (DP) combined with an iterative relaxation strategy. Decremental State Space Relaxation (DSSR) and ngpath relaxation have long been established in the literature as relaxation techniques. In DP algorithms, an effective policy for selecting the next state to extend among the open ones is crucial for performance. In a first exploratory work, we showed that machine learning can be used to identify promising states in DP, Basso and Salani (2026). In particular, if a classifier is trained to identify dominated states in a given DSSR iteration, it can then be used to estimate the quality of the states generated in the subsequent iteration. Building on this idea, in this work we show that it is possible to efficiently embed such a model into a state-of-the-art DP algorithm for the ERCSPP and use its predictions to define a data-driven state exploration policy. Although the approach is data-driven, it remains exact and does not require pre-existing training data. The algorithm has been integrated into the Pathwyse library and tested on a dataset of multi-resource instances. Compared with a node-based extension policy, the proposed approach consistently reduces the number of explored DP states and, for sufficiently difficult instances, also improves runtime.
pdf: https://ssrn.com/abstract=7036722
code: 
arxiv: 
doi: 10.2139/ssrn.7036722
tags:
    - Data-driven optimization
    - Dynamic programming
    - Machine learning
    - Exact methods
plotly: false
---