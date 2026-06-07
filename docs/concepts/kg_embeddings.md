# Knowledge Graph Embeddings

## Overview

This project extends the Football Talent Knowledge Graph with a minimal Knowledge Graph Embedding component based on TransE.

The reasoning system identifies talents using explicit symbolic rules.

The embedding system provides a different capability: it finds players with similar graph representations in a sub-symbolic vector space.

---

## Goal

The goal of the embedding extension is not to replace reasoning, but to complement it.

Reasoning answers questions such as:

* who is a young talented defender?
* who is a hidden talent?

Embeddings answer questions such as:

* which players are structurally similar to this hidden talent?
* which other players look similar in the graph even if they were not selected by the current rules?

This makes the embedding module useful for football scouting and also supports LO1.

---

## Model

The project uses **TransE**, a translation-based Knowledge Graph Embedding model.

TransE learns vector representations for:

* entities
* relations

The basic idea is that a relation should translate one entity vector toward another:

```text
head + relation ~= tail
```

In this project, entities include:

* players
* teams
* leagues
* positions
* inferred talent classes

Relations include:

* `playsFor`
* `playsInLeague`
* `hasPosition`
* `type`

---

## Input Graph for Embeddings

The embedding model is trained on a curated subset of the Knowledge Graph.

Only entity-to-entity triples are exported. Literal triples are excluded.

Examples of exported triples:

```text
Tom_Rothe    playsFor        Union_Berlin
Tom_Rothe    hasPosition     Defender
Union_Berlin playsInLeague   Bundesliga
Tom_Rothe    type            HiddenTalent
```

This design keeps the KGE training graph simple and suitable for a first TransE implementation.

---

## Training Workflow

The embedding workflow consists of three steps:

1. export curated triples from the RDF graph
2. train a TransE model on those triples
3. query similar players from the learned embedding space

Implemented files:

* [src/embeddings/export_triples.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/embeddings/export_triples.py)
* [src/embeddings/train_transe.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/embeddings/train_transe.py)
* [src/embeddings/query_similar_players.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/embeddings/query_similar_players.py)

---

## Example Use Case

The most relevant use case is hidden-talent exploration.

Example workflow:

1. identify a hidden talent using reasoning
2. use the embedding model to retrieve similar players
3. inspect those players as additional scouting candidates

Example:

```text
Hidden Talent:
Tom Rothe

Similarity Query:
Which players have similar graph representations to Tom Rothe?
```

This makes embeddings useful for scouting discovery rather than only for abstract experimentation.

---

## Symbolic vs Sub-Symbolic AI

This project now contains both symbolic and sub-symbolic components.

### Symbolic AI

Implemented through rule-based reasoning.

Examples:

* `Age <= 21`
* `GoalsPer90 >= threshold`
* `TeamStandingRank > 10`

This reasoning is:

* explicit
* interpretable
* easy to justify

### Sub-Symbolic AI

Implemented through TransE embeddings.

This approach is:

* vector-based
* similarity-oriented
* less interpretable than rules

Instead of asking:

```text
Is this player a hidden talent?
```

it asks:

```text
Which players are similar to this player in the graph?
```

This is the core connection between LO1 and the rest of the project.

---

## Limitations

This embedding extension is intentionally minimal.

Important limitations:

* TransE captures graph structure, not full football meaning
* results depend strongly on the curated triples used for training
* similarity does not automatically mean equal football quality
* this is a complement to reasoning, not a replacement for it

For a more advanced extension, the project could later compare TransE with other KGE models such as ComplEx.
