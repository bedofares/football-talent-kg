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

### 2. Run the main pipeline

```powershell
python main.py
```

This runs:

1. preprocessing
2. graph construction
3. reasoning

### 3. Run a single pipeline step if needed

```powershell
python main.py preprocess
python main.py build-graph
python main.py reasoning
```

### 4. Run the optional embeddings workflow

If you want embeddings and similarity search:

```powershell
python main.py embeddings
python main.py all-with-embeddings
python main.py similar-players "Tom Rothe"
```

`embeddings` expects the main graph to already exist.

`all-with-embeddings` runs the full core pipeline first, then the embeddings workflow.

### 5. Run scouting queries

After `python main.py` finishes, the graph is ready for queries.

Examples:

```powershell
python -u "src/queries/query_all_talents.py"
python -u "src/queries/query_hidden_talents.py"
python -u "src/queries/query_talents_by_position.py"
```

### 6. Optional: run the embedding scripts directly

```powershell
python -u "src/embeddings/export_triples.py"
python -u "src/embeddings/train_transe.py"
python -u "src/embeddings/query_similar_players.py" "Tom Rothe"
```

### 7. Verify the pipeline output

You can do a quick verification by:

* checking that [output/football_talent_kg.ttl](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/output/football_talent_kg.ttl) exists
* checking that [data/processed/players_with_standings.csv](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/data/processed/players_with_standings.csv) exists
* running one of the query scripts and confirming it prints results

For a more explicit runbook, see:

* [USAGE.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/USAGE.md)

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

* [docs/concepts/ontology.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/concepts/ontology.md)
* [docs/concepts/rules.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/concepts/rules.md)
* [docs/concepts/kg_architecture.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/concepts/kg_architecture.md)
* [docs/concepts/kg_evolution.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/concepts/kg_evolution.md)
* [docs/analysis/data_model_comparison.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/analysis/data_model_comparison.md)
* [docs/concepts/kg_ml_ai_connection.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/concepts/kg_ml_ai_connection.md)
* [docs/concepts/kg_embeddings.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/docs/concepts/kg_embeddings.md)
* [USAGE.md](D:/TU%20WIEN/Knowledge%20Graphs/football-talent-kg/USAGE.md)

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
