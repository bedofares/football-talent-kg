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

From the project root folder, install the dependencies. The package versions
are pinned in `requirements.txt` so the project uses the same library versions
that were tested during development.

Using a fresh virtual environment is recommended.

On macOS/Linux, create and activate a virtual environment with:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, create and activate a virtual environment with:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
```

On macOS/Linux, run:

```bash
python3 -m pip install -r requirements.txt
```

On Windows, run one of these commands, depending on your Python installation:

```powershell
python -m pip install -r requirements.txt
```

or:

```powershell
py -m pip install -r requirements.txt
```

## 3. Run the Main Pipeline

On macOS/Linux, run:

```bash
python3 main.py
```

On Windows, run one of these commands:

```powershell
python main.py
```

or:

```powershell
py main.py
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
python3 -u src/queries/query_all_talents.py
python3 -u src/queries/query_hidden_talents.py
python3 -u src/queries/query_talents_by_position.py
python3 -u src/queries/query_talents_by_league.py
python3 -u src/queries/query_hidden_talents_by_position.py
python3 -u src/queries/query_hidden_talents_by_league.py
```

These scripts read `output/football_talent_kg.ttl` and print scouting results.

## 5. Run the Embeddings Pipeline

The project also includes a TransE embedding workflow for similar-player
search.

If the main pipeline was already executed, train the embeddings with:

```bash
python3 main.py embeddings
```

On Windows, use:

```powershell
python main.py embeddings
```

or:

```powershell
py main.py embeddings
```

Alternatively, run the full KG pipeline and embeddings together:

```bash
python3 main.py all-with-embeddings
```

Then query similar players:

```bash
python3 main.py similar-players "Tom Rothe"
```

On Windows, use `python` or `py` instead of `python3`.

## 6. Optional: Recreate the FBRef Standings File

This step is not required for normal execution because the ZIP already includes:

```text
data/raw/fbref/standings.csv
```

Only run this command if the standings file needs to be recreated:

```bash
python3 -u src/data_collection/fetch_standings.py
```

This step requires internet access and depends on FBRef and `ScraperFC`.

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
