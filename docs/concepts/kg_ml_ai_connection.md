# Knowledge Graphs, Machine Learning and Artificial Intelligence

## Overview

This project is centered on a Knowledge Graph for football scouting. It integrates structured football data, applies rule-based reasoning, and exposes scouting-oriented graph queries.

The project is not a machine learning system by itself, but it shows clearly how Knowledge Graphs connect to ML and AI.

---

## Knowledge Graph Component

The core representation is an RDF Knowledge Graph containing:

* players
* teams
* leagues
* positions
* player statistics
* team standing ranks

On top of these explicit facts, the graph also contains inferred classes such as:

* `YoungPlayer`
* `YoungTalentedPlayer`
* `YoungTalentedForward`
* `YoungTalentedMidfielder`
* `YoungTalentedDefender`
* `YoungTalentedGoalkeeper`
* `HiddenTalent`

This gives the project a structured and explainable representation of football scouting knowledge.

---

## AI Through Rule-Based Reasoning

The AI component in the current project is rule-based reasoning.

Examples:

```text
Age <= 21
AND Position = Forward
AND 90s >= 10
AND GoalsPer90 >= 0.398
=> YoungTalentedForward
```

```text
YoungTalentedPlayer
AND TeamStandingRank > 10
=> HiddenTalent
```

These inferred classifications are not present in the original CSV files. They are created by the reasoning step based on explicit knowledge and domain rules.

This is an example of explainable AI, because every inferred result can be traced back to transparent human-readable conditions.

---

## Connection to Machine Learning

The project currently uses manually defined thresholds derived from statistical analysis of the dataset.

Machine learning could extend this project in several ways:

* learn talent thresholds automatically from historical player trajectories
* predict the future success probability of young players
* classify players into scouting categories based on historical outcomes

For example, a supervised model could use:

* age
* minutes played
* goals per 90
* assists per 90
* defensive actions per 90
* save percentage
* team strength

to predict whether a player is likely to become an elite professional in later seasons.

In that setup, the Knowledge Graph would provide the structured input features and contextual relationships, while the ML model would provide predictive power.

---

## Connection to Knowledge Graph Embeddings

Knowledge Graph Embeddings (KGEs) transform graph entities and relations into vector representations.

In this project, KGEs could be used in the future to:

* find players similar to already known talents
* recommend transfer targets
* detect promising players that are not captured by the hand-written rules

For example, if several known talents share similar graph neighborhoods, an embedding model could identify other players with comparable structural patterns.

This project does not implement KGEs, but it provides a graph structure that could support them later.

---

## Connection to Graph Neural Networks

Graph Neural Networks (GNNs) learn directly from graph structure.

The player-team-league graph in this project could be used as a basis for a future GNN model. Such a model could combine:

* player statistics
* team context
* league context
* graph relationships

to predict talent status or future player development.

Again, this project does not implement GNNs, but it shows how a structured Knowledge Graph can serve as an input layer for graph-based ML methods.

---

## Why Knowledge Graphs Matter Here

The main strength of the Knowledge Graph in this project is that it acts as an integration and reasoning layer.

It combines:

* data integration from multiple football datasets
* semantic representation through RDF
* rule-based reasoning for talent identification
* query support for scouting services
* future compatibility with ML, KGEs, and GNNs

This makes the graph a useful bridge between symbolic AI, data engineering, and potential future statistical learning methods.
