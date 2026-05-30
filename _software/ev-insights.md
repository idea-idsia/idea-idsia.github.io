---
layout: software
title: EV-Insights
published: true

project_name: "EV-Insights – Open-Source Framework for EV Charging Data Processing, Analysis, and Forecasting"
status: active
start: 2025
end:

short_summary: >
  EV-Insights is an open-source Python framework for electric vehicle
  charging data ingestion, management, analysis, forecasting, and synthetic
  data generation, designed to support research and operational applications
  in smart mobility and energy systems.

image: /assets/images/software/ev-insights.jpg
website: https://link.springer.com/article/10.1186/s42162-025-00615-4
code_repository: https://github.com/EV-Insights
publication: https://link.springer.com/article/10.1186/s42162-025-00615-4
# project_coordinator: IDSIA

aramis_url:
cordis_url:
plotly: false

keywords:
  - Electric Vehicles
  - EV Charging
  - EV Data Management
  - Forecasting
  - Smart Mobility
  - Open Source
  - Machine Learning

contributors:
  - Marco Derboni
  - Matteo Salani

#partners:
#  - IDSIA
#  - SUPSI
---

## Overview

[**EV-Insights**](https://github.com/EV-Insights) is a Python framework designed for the ingestion, management, analysis, visualization, and forecasting of electric vehicle (EV) 
charging data.

The framework integrates functionalities for:

- Ingestion of [historical datasets](https://github.com/EV-Insights/ev-insights/blob/main/doc/tutorials/4.1%20Ingesting%20data%20into%20a%20database/Ingestion%20bulk.md) and [real-time data streams](https://github.com/EV-Insights/ev-insights/blob/main/doc/tutorials/4.1%20Ingesting%20data%20into%20a%20database/Ingestion%20table.md)
- Centralized database management
- Harmonization of heterogeneous public datasets
- Statistical analysis and reporting
- Forecasting of charging demand and usage patterns
- API and CLI-based interaction
- Modular extension through custom services and interfaces

The project is released as **open-source** and is designed to support researchers, charging point operators, DSOs, and developers working on EV charging data.

A detailed description of the framework has been published in the Energy Informatics journal, where the design, architecture, and main functionalities of 
EV-Insights are presented and discussed in detail. The publication provides a comprehensive overview of the framework, including its data ingestion pipeline, 
analytical capabilities, and forecasting modules, together with an evaluation on large-scale real-world EV charging datasets.

_Derboni, M., Salani, M. [EV-Insights: open source framework for electric vehicle charging data processing, analysis, and forecasting.](https://doi.org/10.1186/s42162-025-00615-4) Energy Inform 9, 7 (2026). https://doi.org/10.1186/s42162-025-00615-4_

---

## Motivation

The rapid adoption of electric vehicles and charging infrastructures is generating increasingly large volumes of charging-session data.

These datasets contain valuable information regarding:

- Charging behaviour and user habits
- Energy demand and temporal flexibility
- Infrastructure utilization
- Demand response and smart charging opportunities

However, EV charging data is often fragmented and difficult to use due to:

- Different dataset structures and formats
- Missing or incomplete metadata
- Heterogeneous temporal resolutions
- Data quality inconsistencies
- Limited interoperability across platforms
- Privacy and accessibility constraints

As a result, researchers and operators frequently spend significant effort preprocessing and harmonizing datasets before being able to perform analytics or 
forecasting tasks.

EV-Insights addresses these challenges by providing a unified and extensible framework that simplifies EV charging data processing.

---

## Forecasting and Analytics

EV-Insights includes forecasting services aimed at supporting operational and research applications in smart charging and energy management.

The framework supports:

- Charging demand forecasting
- User-level charging prediction
- Charging station utilization forecasting
- Temporal pattern analysis
- Infrastructure usage statistics
- Load profile analysis

Forecasting pipelines are integrated with MLflow-compatible workflows and can be executed automatically through scheduling services.

The framework also provides APIs and command-line tools for training and inference operations.


---

## Architecture and Functionalities

EV-Insights follows a modular software architecture designed according to software engineering best practices, ensuring maintainability, extensibility, and reproducibility.

![EV-Insights Architecture](/assets/images/software/ev-insights_architecture.png){: width="500"}

---

## Target Users

The framework supports multiple categories of users:


### [Single Users and Operators](https://github.com/EV-Insights/ev-insights/blob/main/doc/tutorials/4.2%20Single%20User/Analysis%20stats%20service.md)

Charging station owners, DSOs, or private users can ingest charging datasets and automatically generate:

- Charging statistics
- Energy usage reports
- Charging session analysis
- User behaviour insights
- Forecasting outputs
- Visual reports in multiple formats

### [Researchers and Data Scientists](https://github.com/EV-Insights/ev-insights/blob/main/doc/tutorials/4.3%20Researchers%20and%20Data%20Scientists/Analysis%20and%20forecasting%20services.md)

Researchers and Data Scientists benefit from significantly reduced effort in data preprocessing and integration, allowing them to focus on modeling, interpretation, 
and methodological development rather than dataset harmonization.
They can combine and harmonize multiple heterogeneous datasets into a unified structure, enabling:

- Cross-dataset analyses
- Benchmarking studies
- Forecasting experiments
- Reproducible scientific workflows

The framework has already been evaluated using more than 3 million charging sessions collected from multiple real-world public datasets, 
demonstrating its capability to scale across diverse data sources and support robust empirical analysis.

### [Developers](https://github.com/EV-Insights/ev-insights/blob/main/doc/tutorials/4.4%20Developers/Developments.md)

Developers can use and extend EV-Insights through:

- Custom ingestion interfaces
- New analysis services
- Forecasting modules
- APIs and integrations
- Database connectors
- Visualization tools

The modular design enables rapid experimentation and integration of new functionalities.

