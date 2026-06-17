---
layout: publication
title: "Rule-based deep reinforcement learning for optimal control of electrical batteries in an energy community"
authors:
  - Roberto Rocchetta
  - Lorenzo Nespoli
  - Vasco Medici
  - Saverio Basso
  - Marco Derboni
  - Matteo Salani
venue: "33rd European Safety and Reliability Conference (ESREL 2023)"
year: 2023
type: conference
abstract: >
  This work investigates rule-based controllers (RBCs) and reinforcement learning (RL) agents for managing distributed electrical batteries in a net-zero 
  energy community (NZEC) and reducing costs and emissions for the community. The RBCs are based on deterministic rules, hence, may fail to adapt to new 
  scenarios and uncertainties. On the other hand, RL agents learn from direct interaction with uncertain environments and can better adapt to new conditions. 
  A novel RL approach is proposed, combining MaskPPO and a deep neural network, to avoid the exploration of unsafe/unprofitable actions and enhance control 
  efficacy through accurate predictions of future demand. These new approaches are demonstrated on the NeurIPS 2022 CityLearn challenge where real-world data 
  from a district in California are embedded within a simulator for distributed battery control. Points of strength and limitations of the different tools 
  discussed. For comparison sake, an oracle-driven controller is also considered as it gives a reference best-achievable optimum for the challenge problem, 
  ie, lower bounds on costs and emissions reduction scores. Based on the results, RL agents generally offered robust control over the distributed batteries 
  and often outperformed the rule-based controllers. Additionally, the combination of action masks and neural forecasters significantly improved the 
  performance of the RL agents, bringing them very close to the scores achieved by the global optimum. A study of the model’s robustness to seasonality 
  changes concludes this work and further illustrates the generalization ability of controllers.
pdf: http://dx.doi.org/10.3850/978-981-18-8071-1_P488-cd
code:
arxiv:
doi:  10.3850/978-981-18-8071-1_P488-cd
tags:
  - Net-zero energy communities
  - Reinforcement Learning
  - Rule-Based control
  - Emissions
  - Peak shaving
  - Uncertainty

plotly: false
---

## BibTeX

```bibtex
    @inproceedings{Rocchetta2023,
      series = {ESREL},
      title = {Rule-Based Deep Reinforcement Learning for Optimal Control of Electrical Batteries in an Energy Community},
      url = {http://dx.doi.org/10.3850/978-981-18-8071-1_P488-cd},
      DOI = {10.3850/978-981-18-8071-1_p488-cd},
      booktitle = {Proceeding of the 33rd European Safety and Reliability Conference},
      publisher = {Research Publishing Services},
      author = {Rocchetta,  Roberto and Nespoli,  Lorenzo and Medici,  Vasco and Basso,  Saverio and Derboni,  Marco and Salani,  Matteo},
      year = {2023},
      pages = {639–646},
      collection = {ESREL}
    }
```
