# Logic-Based Representation Execution Guide

This README explains how to run and inspect the logic-based representation
part of the project.

## Logic Representation

The project uses rule-based reasoning over an RDF Knowledge Graph. The rules
infer new RDF types for players based on age, position, performance metrics,
playing time, and team standing rank.

The logic implementation copy for this assignment section is included in:

```text
src/reasoning.py
```

The query implementation copy for this assignment section is included in:

```text
src/queries/
```

The runnable project is located in:

```text
../2 - construction/
```

## Implemented Rules

The logic rules add inferred classes that are not present in the raw datasets.

Examples:

```text
Age <= 21
=> YoungPlayer
```

```text
Age <= 21
AND hasPosition Forward
AND hasMinutes90s >= 10
AND hasGoalsPer90 >= 0.398
=> YoungTalentedForward
```

```text
Age <= 21
AND hasPosition Midfielder
AND hasMinutes90s >= 10
AND hasGoalContributionsPer90 >= 0.496
=> YoungTalentedMidfielder
```

```text
Age <= 21
AND hasPosition Defender
AND hasMinutes90s >= 10
AND hasDefActionsPer90 >= 2.812
=> YoungTalentedDefender
```

```text
YoungTalentedPlayer
AND hasStandingRank > 10
=> HiddenTalent
```

These rules evolve the Knowledge Graph by adding new inferred RDF type triples,
for example:

```text
Tom_Rothe rdf:type YoungTalentedDefender
Tom_Rothe rdf:type YoungTalentedPlayer
Tom_Rothe rdf:type HiddenTalent
```

## Run the Logic Workflow

Go to the runnable construction folder and run the full pipeline:

```bash
cd "../2 - construction"
python3 main.py
```

On Windows, use:

```powershell
python main.py
```

or:

```powershell
py main.py
```

This executes:

1. preprocessing
2. RDF graph construction
3. rule-based reasoning

The reasoning step updates:

```text
../2 - construction/output/football_talent_kg.ttl
```

## Run Reasoning Only

If the graph already exists and only the reasoning step should be rerun:

```bash
cd "../2 - construction"
python3 main.py reasoning
```

On Windows, use `python` or `py` instead of `python3`.

## Run Logic Query Examples

After the graph has been constructed and reasoning has been applied, run:

```bash
cd "../2 - construction"
python3 -u src/queries/query_all_talents.py
python3 -u src/queries/query_talents_by_position.py
python3 -u src/queries/query_talents_by_league.py
python3 -u src/queries/query_hidden_talents.py
python3 -u src/queries/query_hidden_talents_by_position.py
python3 -u src/queries/query_hidden_talents_by_league.py
```

These queries retrieve inferred scouting categories such as young talented
players, position-specific talents, and hidden talents.

## Validate Logic Results

Useful validation scripts are:

```bash
cd "../2 - construction"
python3 -u src/validation/validate_graph_counts.py
python3 -u src/validation/explore_reasoning_results.py
```

## Notes

The logic-based representation is transparent and explainable because each
classification follows explicit rules.

The main limitation is that the quality of the results depends on manually
chosen thresholds and on the quality of the input statistics. Changing the
thresholds can change which players are inferred as talents or hidden talents.
