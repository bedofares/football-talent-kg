# Knowledge Graph Evolution

## Overview

Knowledge Graph evolution describes how a graph is updated, corrected, and enriched over time as new information becomes available or data quality issues are discovered.

In this project, KG evolution happens in three main ways:

* raw football data is integrated into the graph
* inconsistent or incomplete source data is corrected during preprocessing
* new knowledge is added through reasoning rules

---

## 1. Updating the Graph with New Data

The graph is built from external football datasets:

* player statistics
* league standings

When a new season, updated standings, or refreshed player statistics become available, the pipeline can be run again:

1. collect or replace the raw data
2. preprocess and merge the datasets
3. rebuild the RDF graph
4. rerun reasoning

This is a form of KG evolution because the graph content changes when the underlying football data changes.

---

## 2. Correcting the Graph

KG evolution also includes correcting errors and inconsistencies before they enter the final graph.

Examples from this project:

* fixing encoding issues in team names such as accented characters
* aligning team names between player and standings datasets
* normalizing league names before merging datasets
* correcting path and import issues in the processing pipeline
* handling duplicate player entries during validation

These corrections improve graph quality and prevent incorrect or missing RDF triples.

---

## 3. Enriching the Graph Through Reasoning

The initial graph contains explicit facts such as:

* player name
* age
* club
* league
* position
* performance statistics
* team standing rank

After reasoning, the graph evolves further by adding inferred classes:

* `YoungPlayer`
* `YoungTalentedPlayer`
* `YoungTalentedForward`
* `YoungTalentedMidfielder`
* `YoungTalentedDefender`
* `YoungTalentedGoalkeeper`
* `HiddenTalent`

This is an important form of KG evolution because the graph is not only updated with new raw data, but also enriched with higher-level knowledge derived from rules.

---

## 4. Completing Missing Knowledge

The source datasets do not directly contain concepts such as:

* young talent
* hidden talent
* position-specific talent classes

These concepts are created through preprocessing, threshold calculation, and reasoning.

As a result, the final graph contains knowledge that was not explicitly present in the raw CSV files. This is a form of knowledge completion.

---

## 5. Why KG Evolution Matters in This Project

KG evolution is important here because football scouting is dynamic:

* player performance changes over time
* league tables change over time
* talent status may change over time
* hidden talents may become widely recognized later

A useful scouting graph must therefore be able to evolve as the underlying football world changes.

---

## Conclusion

In this project, Knowledge Graph evolution is implemented through:

* updating the graph when new football data is available
* correcting data inconsistencies during preprocessing and validation
* enriching the graph with inferred talent categories
* completing missing knowledge that is not directly stored in the original datasets

This shows that the graph is not static. It is a living representation of the scouting domain that can be rebuilt, corrected, and extended over time.
