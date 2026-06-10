---
layout: publication
title: Using Structural and Semantic Information to Identify Software Components
authors:
    - Cezar Sas
    - Andrea Capiluppi
year: 2021
type: conference
venue: 2021 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER)
abstract:
    Component Based Software Engineering (CBSE) seeks to promote the reuse of
    software by using existing software modules into the development process. However,
    the availability of such a reusable component is not immediate and is costly and
    time consuming. As an alternative, the extraction from preexisting OO software can
    be considered.In this work, we evaluate two community detection algorithms for the
    task of software components identification. Considering `components' as `communities',
    the aim is to evaluate how independent, yet cohesive, the components are when extracted
    by structurally informed algorithms.We analyze 412 Java systems and evaluate the
    cohesion of the extracted communities using four document representation techniques.
    The evaluation aims to find which algorithm extracts the most semantically cohesive,
    yet separated communities.The results show a good performance in both algorithms,
    however, each has its own strengths. Leiden extracts less cohesive, but better separated,
    and better clustered components that depend more on similar ones. Infomap, on the
    other side, creates more cohesive, slightly overlapping clusters that are less likely
    to depend on other semantically similar components.
doi: 10.1109/SANER50967.2021.00063
arxiv: "2102.04710"
pdf: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9425947
tags:
    - Software Engineering
    - Mining Software Repositories
    - Component Identification
---
