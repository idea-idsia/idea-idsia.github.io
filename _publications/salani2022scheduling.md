---
layout: publication
title: "Scheduling the energy consumption of residential loads, the impact of missing data"
authors:
  - Matteo Salani
  - Marco Derboni
  - Andrea Emilio Rizzoli
venue:
year: 2022
type: abstract
abstract: >
  One of the tasks of early response groups to threats, especially in urban areas, is to quickly trace
  the source of the danger and take appropriate steps to prevent its effects. For example, in the case of
  atmospheric contamination, the first thread indicators are the concentrations of the dangerous substance
  reported by a network of sensors in a given area. Thus, the dedicated emergency system should localize the
  source of contamination based on the data from the sensors. Moreover, such a system should work in realtime. 
  The paper presents the reconstruction system pointing to the most probable source of the airborne
  toxin in the urban terrain in real-time. The method is based on the stochastic event reconstruction approach
  using the Approximate Bayesian Computation (ABC) methodology. The sequential ABC scanning algorithm
  dynamically updates the posterior distributions of the searched parameters by the most up-to-date
  reported concentrations. The operation of such a system in real-time is possible thanks to the use of the
  surrogate model in place of the computationally expensive urban dispersion model. The surrogate model
  exploits the feedforward neural network (FFNN) characterizing with the fast reply. The process of training
  dedicated FFNN and methods of FFNN model verification for the system dedicated to the given urbanized
  area is presented. Training of the artificial neural network requires an extensive, reliable set of contaminant
  dispersion data, impossible to obtain from actual field experiments. Thus, the training dataset was
  generated using the Quick Urban Industrial Complex Dispersion Modeling system (QUIC), developed by Los
  Alamos National Laboratory. Finally, the proposed reconstruction system's efficiency is tested using
  synthetic releases and actual data from a full-scale field experiment DAPPLE conducted in central London
  in 2007.
pdf: https://scholarsarchive.byu.edu/iemssconference/2022/Stream-B/19/
code:
arxiv:
doi:
tags:
  - Real-time emergency system
  - Stochastic event reconstruction
  - Artificial neural network
  - Airborne
  - Toxin dispersion
---

## BibTeX

```bibtex
    @inproceedings{salani2022scheduling,
      title     = {Scheduling the Energy Consumption of Residential Loads, the Impact of Missing Data},
      author    = {Salani, Matteo and Derboni, Marco and Rizzoli, Andrea Emilio},
      booktitle = {Proceedings of the 11th International Congress on Environmental Modelling and Software (iEMSs 2022)},
      series    = {iEMSs Conference},
      year      = {2022},
      address   = {Brussels, Belgium},
      url       = {https://scholarsarchive.byu.edu/iemssconference/2022/Stream-B/19/}
    }
```
