# How to Execute the KG Construction Code

This README explains how to run the code included in the `2 - construction`
submission folder.

## 1. Required Files

The ZIP already includes the code and data needed to run the project. The
expected structure is:

```text
main.py
requirements.txt
src/
data/raw/fbref/standings.csv
data/raw/kaggle/players_data_light-2025_2026.csv
```

The Kaggle link is provided only for provenance and reproducibility:

```text
https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2025-2026
```

The included `standings.csv` file was generated from FBRef using:

```text
src/data_collection/fetch_standings.py
```

## 2. Install Dependencies

From the project root folder, run:

```bash
python -m pip install -r requirements.txt
```

## 3. Run the Main Pipeline

Run:

```bash
python main.py
```

This executes the construction pipeline:

1. preprocesses and merges the raw datasets
2. creates derived football features
3. constructs the RDF Knowledge Graph
4. applies rule-based reasoning

The main output is:

```text
output/football_talent_kg.ttl
```

## 4. Run Query Examples

After the pipeline finishes, run example query scripts:

```bash
python -u src/queries/query_all_talents.py
python -u src/queries/query_hidden_talents.py
python -u src/queries/query_talents_by_position.py
python -u src/queries/query_talents_by_league.py
python -u src/queries/query_hidden_talents_by_position.py
python -u src/queries/query_hidden_talents_by_league.py
```

These scripts read `output/football_talent_kg.ttl` and print scouting results.

## 5. Optional: Recreate the FBRef Standings File

This step is not required for normal execution because the ZIP already includes:

```text
data/raw/fbref/standings.csv
```

Only run this command if the standings file needs to be recreated:

```bash
python -u src/data_collection/fetch_standings.py
```

This step requires internet access and depends on FBRef and `ScraperFC`.

## 6. Optional: Run Knowledge Graph Embeddings

To train the optional TransE embeddings:

```bash
python main.py embeddings
```

Or run the full pipeline including embeddings:

```bash
python main.py all-with-embeddings
```

Then query similar players:

```bash
python main.py similar-players "Tom Rothe"
```

## 7. Expected Results

After running the core pipeline, these files should exist:

```text
data/processed/players_with_standings.csv
output/football_talent_kg.ttl
```

If embeddings are also executed, these files/folders should exist:

```text
data/processed/kg_triples.tsv
output/transe_model/
```
