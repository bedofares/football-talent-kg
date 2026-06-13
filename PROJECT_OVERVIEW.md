# Football Talent Knowledge Graph

## Main Idea

This project builds a Knowledge Graph for football scouting.

The goal is simple:

* take football player data
* combine it with team standings
* build a Knowledge Graph
* use rules to identify:
  * young players
  * young talented players
  * hidden talents

In short, the project tries to answer:

```text
Which young football players look promising?
Which of them may be overlooked because they play for weaker teams?
```

---

## What the Project Does

The project starts from raw football data in CSV format.

Then it:

1. cleans and merges the data
2. creates useful football features such as `GoalsPer90`
3. builds an RDF Knowledge Graph
4. applies reasoning rules
5. runs scouting-style queries on the graph
6. optionally trains embeddings for player similarity

---

## Data Sources

This project uses two data sources.

1. **Football Players Stats 2025/2026** from Kaggle:
   https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2025-2026

   The player CSV should be placed at:

   ```text
   data/raw/kaggle/players_data_light-2025_2026.csv
   ```

2. **Team standings from FBRef**

   The standings data was collected from FBRef using `ScraperFC`, because the required league tables were not available as a direct CSV download.

   The scraper is located at:

   ```text
   src/data_collection/fetch_standings.py
   ```

   It creates:

   ```text
   data/raw/fbref/standings.csv
   ```

   The scraped leagues are Premier League, La Liga, Bundesliga, Serie A, and Ligue 1 for the 2025/2026 season.

---

## Project Flow

The full flow is:

```text
Raw Football Data
    ->
Preprocessing
    ->
Processed Dataset
    ->
Knowledge Graph Construction
    ->
Reasoning
    ->
Talents and Hidden Talents
    ->
Queries and Validation
    ->
Optional TransE Embeddings for Similar Player Search
```

---

## What Is Inside the Graph

The graph contains:

* players
* teams
* leagues
* positions
* team standing ranks
* player performance features

It also contains inferred classes such as:

* `YoungPlayer`
* `YoungTalentedPlayer`
* `YoungTalentedForward`
* `YoungTalentedMidfielder`
* `YoungTalentedDefender`
* `YoungTalentedGoalkeeper`
* `HiddenTalent`

These inferred classes are created by rules, not taken directly from the source data.

---

## Why This Is Useful

A normal table gives raw player statistics.

This project adds more structure and meaning:

* a player is connected to a team
* a team is connected to a league
* a player has one or more positions
* a player can be inferred to be talented or hidden talent

That makes the data easier to query in a scouting-oriented way.

Examples:

* show all talented defenders
* show hidden talents by league
* show all talents in Bundesliga
* show players similar to a hidden talent using embeddings

---

## Main Files

### Core pipeline

* [src/preprocess.py](src/preprocess.py)
  cleans, merges, and enriches the raw data

* [src/build_graph.py](src/build_graph.py)
  builds the RDF Knowledge Graph

* [src/reasoning.py](src/reasoning.py)
  applies rule-based reasoning to infer talent classes

### Scouting queries

* [src/queries/query_all_talents.py](src/queries/query_all_talents.py)
* [src/queries/query_talents_by_position.py](src/queries/query_talents_by_position.py)
* [src/queries/query_talents_by_league.py](src/queries/query_talents_by_league.py)
* [src/queries/query_hidden_talents.py](src/queries/query_hidden_talents.py)
* [src/queries/query_hidden_talents_by_position.py](src/queries/query_hidden_talents_by_position.py)
* [src/queries/query_hidden_talents_by_league.py](src/queries/query_hidden_talents_by_league.py)

### Embeddings

* [src/embeddings/export_triples.py](src/embeddings/export_triples.py)
* [src/embeddings/train_transe.py](src/embeddings/train_transe.py)
* [src/embeddings/query_similar_players.py](src/embeddings/query_similar_players.py)

---

## How to Run the Project

For setup, execution commands, query examples, and embedding examples, see
[README.md](README.md).

---

## Outputs

Important output files:

* processed data:
  [data/processed/players_with_standings.csv](data/processed/players_with_standings.csv)

* Knowledge Graph:
  [output/football_talent_kg.ttl](output/football_talent_kg.ttl)

* embedding training triples:
  [data/processed/kg_triples.tsv](data/processed/kg_triples.tsv)

* embedding artifacts:
  [output/transe_model](output/transe_model)

---

## Documentation

More details are available in:

* [docs/concepts/ontology.md](docs/concepts/ontology.md)
* [docs/concepts/rules.md](docs/concepts/rules.md)
* [docs/concepts/kg_architecture.md](docs/concepts/kg_architecture.md)
* [docs/concepts/kg_evolution.md](docs/concepts/kg_evolution.md)
* [docs/analysis/data_model_comparison.md](docs/analysis/data_model_comparison.md)
* [docs/concepts/kg_ml_ai_connection.md](docs/concepts/kg_ml_ai_connection.md)
* [docs/concepts/kg_embeddings.md](docs/concepts/kg_embeddings.md)
* [README.md](README.md)

---

## Short Summary

This project turns football data into a Knowledge Graph for scouting.

It combines:

* data preprocessing
* RDF graph construction
* rule-based reasoning
* scouting queries
* optional TransE embeddings

The main outcome is a graph that helps identify promising young players and hidden talents in a structured and explainable way.
