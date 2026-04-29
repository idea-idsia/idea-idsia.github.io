---
layout: publication
title:
    "GitRanking: A ranking of GitHub topics for software classification using active
    sampling"
authors:
    - Cezar Sas
    - Andrea Capiluppi
    - Claudio Di Sipio
    - Juri Di Rocco
    - Davide Di Ruscio
year: 2023
type: journal
venue: Software Practice and Experience
abstract:
    "Abstract Context GitHub is the world's most prominent host of source code,
    with more than 327M repositories. However, most of these repositories are not labelled
    or inadequately, making it harder for users to find relevant projects. Various proposals
    for software application domain classification over the past years have been proposed.
    However, these several of those approaches suffer from multiple issues, called antipatterns
    of software classification, that reduce their usability. Objective In this paper,
    we propose a new taxonomy in the GitHub ecosystem, called GitRanking, starting from
    a well‐structured data set, composed of curated repositories annotated with topics.
    The main objective is to create a baseline methodology for software classification
    that is expandable, hierarchical, grounded in a knowledge base, and free of antipatterns.
    Method We collected 121K topics from GitHub and used GitRanking to create a taxonomy
    of 301 ranked application domains. GitRanking (1) uses active sampling to ensure
    a minimal number of annotations to create the ranking; and (2) links each topic
    to Wikidata, reducing ambiguities and improving the reusability of the taxonomy.
    Furthermore, we adopt the conceived taxonomy in a classification task by considering
    a state‐of‐the‐art classifier. Results Our results show that GitRanking can effectively
    rank terms in a hierarchy according to how general or specific their meaning is.
    Furthermore, we show that GitRanking is a dynamically extensible method: it can
    currently accept further terms to be ranked, and with a minimum number of annotations
    (). Concerning the classification task, we show that the model achieves an F1‐score
    of 34%, with a precision of 54%. Conclusion This paper is the first collective attempt
    at building a ground‐up taxonomy of software domains. Our vision is that our taxonomy,
    and its extensibility, can be used to better and more precisely label software projects."
doi: 10.1002/spe.3238
pdf: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/spe.3238
tags:
    - Software Engineering Research
    - Topic Modeling
    - Wikis in Education and Collaboration
---
