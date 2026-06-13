# Embeddings Module

This module adds a minimal Knowledge Graph Embedding extension to the project.

Workflow:

1. run `export_triples.py` to create a curated KGE training graph
2. run `train_transe.py` to train a TransE model
3. run `query_similar_players.py "Player Name"` to retrieve similar players

Files:

* `export_triples.py`: exports entity-to-entity triples for KGE training
* `train_transe.py`: trains TransE and stores embeddings
* `query_similar_players.py`: similarity search over player embeddings
