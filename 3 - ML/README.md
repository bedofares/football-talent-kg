# ML-Based Representation Execution Guide

This README explains how to run the ML-based representation part of the
project.

## ML Representation

The project uses a TransE-style Knowledge Graph Embedding model.

The embedding model learns vector representations for graph entities and
relations. In this project, entities include players, teams, leagues,
positions, and inferred talent classes. Relations include:

```text
playsFor
playsInLeague
hasPosition
type
```

The embeddings are used for similar-player search. For example, after training
the model, the project can retrieve players that are structurally similar to a
selected player such as `Tom Rothe`, `Lamine Yamal`, `Arda Güler`, or
`Rayan Cherki`.

## Implemented Files

The ML implementation copy for this assignment section is included in:

```text
src/embeddings/export_triples.py
src/embeddings/train_transe.py
src/embeddings/query_similar_players.py
```

The runnable project is located in:

```text
../2 - construction/
```

## Required Previous Step

Before running embeddings, go to the runnable construction folder and construct
the Knowledge Graph:

```bash
cd "../2 - construction"
python3 main.py
```

On Windows, use `python` or `py` instead of `python3`.

This creates:

```text
../2 - construction/output/football_talent_kg.ttl
```

## Run the Embeddings Workflow

After the Knowledge Graph exists, run:

```bash
cd "../2 - construction"
python3 main.py embeddings
```

This executes:

1. triple export from the RDF Knowledge Graph
2. TransE training
3. saving embedding artifacts

The generated files are:

```text
../2 - construction/data/processed/kg_triples.tsv
../2 - construction/output/transe_model/entity_embeddings.pt
../2 - construction/output/transe_model/entity_to_id.json
../2 - construction/output/transe_model/relation_to_id.json
```

Alternatively, run the full KG pipeline and embeddings together:

```bash
cd "../2 - construction"
python3 main.py all-with-embeddings
```

## Query Similar Players

After training the embeddings, run examples such as:

```bash
cd "../2 - construction"
python3 main.py similar-players "Tom Rothe"
python3 main.py similar-players "Lamine Yamal"
python3 main.py similar-players "Arda Güler"
python3 main.py similar-players "Rayan Cherki"
```

On Windows, use:

```powershell
python main.py similar-players "Tom Rothe"
```

or:

```powershell
py main.py similar-players "Tom Rothe"
```

## Notes

The embedding model does not replace the rule-based reasoning system. It
complements it by supporting similarity-based exploration of players in the
Knowledge Graph.

The embeddings are trained from the constructed graph, so if the graph changes,
the embedding workflow should be rerun.
