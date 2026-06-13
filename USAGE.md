# Usage

This file explains what to run, in what order, and how to verify that the project worked.

---

## Recommended Workflow

From the repository root:

```powershell
python3 -m pip install -r requirements.txt
python3 main.py
```

`python3 main.py` is the main entry point for the project.

It runs:

1. preprocessing
2. knowledge graph construction
3. reasoning

After that, the graph is ready for queries.

---

## Run Individual Steps

If you only want one stage:

```powershell
python3 main.py preprocess
python3 main.py build-graph
python3 main.py reasoning
```

Use this when:

* you changed preprocessing logic and want to rebuild the processed dataset
* you changed graph construction and want to regenerate the RDF graph
* you changed rules or thresholds and only want to rerun reasoning

---

## Run Optional Embeddings

Embeddings are optional and are not part of the default `python3 main.py` flow.

Use:

```powershell
python3 main.py embeddings
python3 main.py all-with-embeddings
python3 main.py similar-players "Tom Rothe"
```

Meaning:

* `embeddings` runs triple export plus TransE training
* `all-with-embeddings` runs the full core pipeline and then embeddings
* `similar-players` queries the trained embedding model

If you already ran `python3 main.py`, then `python3 main.py embeddings` is enough.

---

## Run Queries

After the pipeline is ready, run query scripts such as:

```powershell
python3 -u "src/queries/query_all_talents.py"
python3 -u "src/queries/query_hidden_talents.py"
python3 -u "src/queries/query_talents_by_position.py"
python3 -u "src/queries/query_talents_by_league.py"
python3 -u "src/queries/query_hidden_talents_by_position.py"
python3 -u "src/queries/query_hidden_talents_by_league.py"
```

---

## Verify the Output

Minimum verification:

1. Confirm the processed dataset exists:
   [data/processed/players_with_standings.csv](data/processed/players_with_standings.csv)
2. Confirm the graph exists:
   [output/football_talent_kg.ttl](output/football_talent_kg.ttl)
3. Run a query and confirm it prints player results.

Better verification:

```powershell
python3 -u "src/validation/validate_graph_counts.py"
python3 -u "src/validation/validate_team_matching.py"
```

You can also inspect:

```powershell
python3 -u "src/validation/explore_reasoning_results.py"
python3 -u "src/validation/explore_statistics.py"
```

---

## Optional Embeddings Workflow

If you want player similarity search:

```powershell
python3 main.py embeddings
python3 main.py similar-players "Tom Rothe"
```

You can still run the embedding scripts directly:

```powershell
python3 -u "src/embeddings/export_triples.py"
python3 -u "src/embeddings/train_transe.py"
python3 -u "src/embeddings/query_similar_players.py" "Tom Rothe"
```

This workflow is optional and not required for the core knowledge graph pipeline.
