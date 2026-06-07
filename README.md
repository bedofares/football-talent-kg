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

* [src/preprocess.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/preprocess.py)
  cleans, merges, and enriches the raw data

* [src/build_graph.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/build_graph.py)
  builds the RDF Knowledge Graph

* [src/reasoning.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/reasoning.py)
  applies rule-based reasoning to infer talent classes

### Scouting queries

* [src/queries/query_all_talents.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries/query_all_talents.py)
* [src/queries/query_talents_by_position.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries/query_talents_by_position.py)
* [src/queries/query_talents_by_league.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries/query_talents_by_league.py)
* [src/queries/query_hidden_talents.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries/query_hidden_talents.py)
* [src/queries/query_hidden_talents_by_position.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries/query_hidden_talents_by_position.py)
* [src/queries/query_hidden_talents_by_league.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/queries/query_hidden_talents_by_league.py)

### Embeddings

* [src/embeddings/export_triples.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/embeddings/export_triples.py)
* [src/embeddings/train_transe.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/embeddings/train_transe.py)
* [src/embeddings/query_similar_players.py](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/src/embeddings/query_similar_players.py)

---

## How to Run the Project

### 1. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2. Preprocess the raw data

```powershell
python -u "src/preprocess.py"
```

### 3. Build the Knowledge Graph

```powershell
python -u "src/build_graph.py"
```

### 4. Run reasoning

```powershell
python -u "src/reasoning.py"
```

### 5. Run scouting queries

Examples:

```powershell
python -u "src/queries/query_all_talents.py"
python -u "src/queries/query_hidden_talents.py"
python -u "src/queries/query_talents_by_position.py"
```

### 6. Optional: run the embedding pipeline

```powershell
python -u "src/embeddings/export_triples.py"
python -u "src/embeddings/train_transe.py"
python -u "src/embeddings/query_similar_players.py" "Tom Rothe"
```

---

## Outputs

Important output files:

* processed data:
  [data/processed/players_with_standings.csv](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/data/processed/players_with_standings.csv)

* Knowledge Graph:
  [output/football_talent_kg.ttl](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/output/football_talent_kg.ttl)

* embedding training triples:
  [data/processed/kg_triples.tsv](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/data/processed/kg_triples.tsv)

* embedding artifacts:
  [output/transe_model](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/output/transe_model)

---

## Documentation

More details are available in:

* [docs/ontology.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/ontology.md)
* [docs/rules.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/rules.md)
* [docs/kg_architecture.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/kg_architecture.md)
* [docs/kg_evolution.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/kg_evolution.md)
* [docs/data_model_comparison.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/data_model_comparison.md)
* [docs/kg_ml_ai_connection.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/kg_ml_ai_connection.md)
* [docs/kg_embeddings.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/kg_embeddings.md)

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
