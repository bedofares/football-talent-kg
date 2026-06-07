# Knowledge Graph Architecture

## Overview

The Football Talent Knowledge Graph is implemented as a small pipeline architecture with four main stages:

1. data preparation
2. graph construction
3. reasoning
4. query and validation services

This architecture is intentionally simple, modular, and easy to explain in a portfolio setting.

---

## Architecture Components

### 1. Raw Data Layer

Input data is stored as CSV files:

* player statistics
* team standings

These files provide the factual input for the system.

### 2. Preprocessing Layer

Implemented in [src/preprocess.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/preprocess.py).

Responsibilities:

* load raw datasets
* normalize league names
* merge player and standings data
* compute derived features such as `GoalsPer90` and `DefActionsPer90`
* export a cleaned processed dataset

This layer performs data integration and feature creation before graph construction.

### 3. Graph Construction Layer

Implemented in [src/build_graph.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/build_graph.py).

Responsibilities:

* create RDF resources for players, teams, leagues, and positions
* create core class hierarchy
* add literals and relationships
* serialize the graph to Turtle

This layer converts tabular processed data into a semantic graph representation.

### 4. Reasoning Layer

Implemented in [src/reasoning.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/reasoning.py).

Responsibilities:

* load the RDF graph
* apply rule-based talent classification
* infer `YoungPlayer`, `YoungTalentedPlayer`, and `HiddenTalent` classes
* write the enriched graph back to disk

This layer is where the graph becomes more than a data container and starts providing AI-style inference.

### 5. Query and Validation Layer

Implemented in:

* [src/queries](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries)
* [src/validation](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/validation)

Responsibilities:

* expose scouting-oriented graph queries
* inspect talent counts and graph statistics
* validate preprocessing assumptions and reasoning results

This layer provides services on top of the KG.

---

## Why This Architecture Fits the Project

This architecture is appropriate because the project goal is not only to store data, but to transform and enrich it step by step.

It supports:

* separation of concerns
* easier debugging
* transparent reasoning
* reproducible graph rebuilding

The architecture also makes it clear which tasks are handled by:

* preprocessing code
* graph modeling
* reasoning rules
* query scripts

This is important for LO5 because it shows that the KG is part of an overall system architecture rather than a single isolated file.
