---
layout: publication
title: Weak Labelling for File-level Source Code Classification
authors:
    - Cezar Sas
    - Andrea Capiluppi
year: 2023
type: conference
abstract:
    Software repository hosting services contain large amounts of open-source
    software, with GitHub hosting over 200 million repositories, from new to established
    ones. However, these repositories are not easy to find, calling for various attempts
    to classify their application domains automatically. However, most proposed approaches
    use artifacts, like README files, as a proxy for the project, losing the information
    in the source code and the interaction between files. Furthermore, they all focus
    on the project-level, ignoring the decomposition of software projects into components
    and modules.This work presents a weak labelling approach based on keyword extraction
    to annotate source files in a software project.Our findings suggest that using keywords
    to perform file-level annotations is an effective approach that can capture enough
    information from the source file so that new labels can be predicted.The long-term
    goal of our research is to classify source code files and use these annotations
    to identify semantic components in software projects. In addition, these annotations
    can be used for semantic reverse engineering, software reuse, and more. We plan
    to train machine learning models that use our proposed weak supervision to better
    annotate source files inside software projects.
doi: 10.1109/SANER56733.2023.00074
pdf: https://ieeexplore.ieee.org/document/10123683
tags:
    - Software Engineering
    - AI4SE
    - Software Classification
---
