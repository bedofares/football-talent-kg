# Knowledge Graph Data Model Comparison

## Overview

This project mainly uses the RDF data model, but it can be compared to other common ways of representing Knowledge Graphs.

This comparison supports the understanding of LO4 by showing why RDF was chosen and how it differs from other models.

---

## 1. Relational / Database View

In a relational database, the project data would naturally be stored in tables such as:

* `Players`
* `Teams`
* `Leagues`
* `Standings`

This model is strong for:

* efficient tabular storage
* joins
* data cleaning and preprocessing

This is exactly the role played by the CSV and pandas preprocessing stage in this project.

Weaknesses for this project:

* inferred classes such as `HiddenTalent` are less natural to represent
* semantic relationships and class hierarchies are not first-class concepts
* graph-style traversal is less explicit

---

## 2. Semantic Web / RDF View

The final project graph uses RDF triples:

* subject
* predicate
* object

Examples:

```text
LamineYamal -> playsFor -> Barcelona
Barcelona -> playsInLeague -> LaLiga
LamineYamal -> rdf:type -> YoungTalentedForward
```

Strengths of RDF for this project:

* natural representation of entities and relationships
* easy addition of inferred types
* direct support for graph queries
* clear separation between explicit and inferred knowledge

This is why RDF is the most suitable final model for the scouting KG.

---

## 3. Machine Learning View

From a machine learning perspective, the same domain would often be represented as a feature matrix.

Each player would become a row with columns such as:

* age
* goals per 90
* assists per 90
* defensive actions per 90
* save percentage
* team rank

This representation is strong for:

* prediction
* classification
* clustering

Weaknesses for this project:

* it loses explicit graph structure
* team-league-player relationships are flattened
* inferred semantic classes are not naturally represented as graph knowledge

---

## 4. Graph ML / Embedding View

In Knowledge Graph Embeddings or Graph Neural Networks, graph entities and relations are represented in vector form.

This is useful for:

* similarity search
* recommendation
* link prediction
* downstream prediction tasks

However, this representation is not directly human-readable and is not the main focus of this project.

In this project, such models are relevant as future extensions rather than the primary representation.

---

## Why RDF Was Chosen

The project combines multiple stages:

* tabular preprocessing
* semantic graph construction
* rule-based reasoning
* scouting queries

Because of this, RDF is the best final data model:

* relational-style data handling is used during preprocessing
* RDF is used for the final Knowledge Graph
* ML-style representations are discussed as possible extensions

This shows how different KG-related data models connect, and why the RDF model is the most appropriate final representation for the current project.
