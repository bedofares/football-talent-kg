# Usage

This file explains what to run, in what order, and how to verify that the project worked.

---

## Recommended Workflow

From the repository root:

```powershell
python -m pip install -r requirements.txt
python main.py
```

`python main.py` is the main entry point for the project.

It runs:

1. preprocessing
2. knowledge graph construction
3. reasoning

After that, the graph is ready for queries.

---

## Run Individual Steps

If you only want one stage:

```powershell
python main.py preprocess
python main.py build-graph
python main.py reasoning
```

Use this when:

* you changed preprocessing logic and want to rebuild the processed dataset
* you changed graph construction and want to regenerate the RDF graph
* you changed rules or thresholds and only want to rerun reasoning

---

## Run Optional Embeddings

Embeddings are optional and are not part of the default `python main.py` flow.

Use:

```powershell
python main.py embeddings
python main.py all-with-embeddings
python main.py similar-players "Tom Rothe"
```

Meaning:

* `embeddings` runs triple export plus TransE training
* `all-with-embeddings` runs the full core pipeline and then embeddings
* `similar-players` queries the trained embedding model

If you already ran `python main.py`, then `python main.py embeddings` is enough.

---

## Run Queries

After the pipeline is ready, run query scripts such as:

```powershell
python -u "src/queries/query_all_talents.py"
python -u "src/queries/query_hidden_talents.py"
python -u "src/queries/query_talents_by_position.py"
python -u "src/queries/query_talents_by_league.py"
python -u "src/queries/query_hidden_talents_by_position.py"
python -u "src/queries/query_hidden_talents_by_league.py"
```

---

## Verify the Output

Minimum verification:

1. Confirm the processed dataset exists:
   [data/processed/players_with_standings.csv](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/data/processed/players_with_standings.csv)
2. Confirm the graph exists:
   [output/football_talent_kg.ttl](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/output/football_talent_kg.ttl)
3. Run a query and confirm it prints player results.

Better verification:

```powershell
python -u "src/validation/validate_graph_counts.py"
python -u "src/validation/validate_team_matching.py"
```

You can also inspect:

```powershell
python -u "src/validation/explore_reasoning_results.py"
python -u "src/validation/explore_statistics.py"
```

---

## Optional Embeddings Workflow

If you want player similarity search:

```powershell
python main.py embeddings
python main.py similar-players "Tom Rothe"
```

You can still run the embedding scripts directly:

```powershell
python -u "src/embeddings/export_triples.py"
python -u "src/embeddings/train_transe.py"
python -u "src/embeddings/query_similar_players.py" "Tom Rothe"
```

This workflow is optional and not required for the core knowledge graph pipeline.
