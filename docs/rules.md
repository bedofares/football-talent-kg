# Talent Identification Rules

## Rule Design Principles

The goal is to identify genuinely promising young players while ensuring fair comparisons across positions and avoiding misleading statistics from players with very limited playing time.

To achieve this, all talent classifications:

* Require a minimum amount of playing time.
* Use position-specific performance metrics.
* Compare players against others in the same position.
* Use percentile-based thresholds instead of arbitrary values.

---

# Derived Metrics

The following metrics are computed during preprocessing.

## GoalsPer90

GoalsPer90 = Goals / 90s

Measures scoring efficiency independently of total playing time.

---

## AssistsPer90

AssistsPer90 = Assists / 90s

Measures chance creation efficiency independently of total playing time.

---

## GoalContributionsPer90

GoalContributionsPer90 = (Goals + Assists) / 90s

Measures total attacking contribution.

---

## DefActions

DefActions = Tackles Won + Interceptions

Measures defensive involvement.

---

## DefActionsPer90

DefActionsPer90 = DefActions / 90s

Measures defensive effectiveness independently of total playing time.

---

# Eligibility Rule

## Eligible Player

A player must have:

90s >= 10

Rationale:

Players with very limited minutes may have misleading statistics that do not accurately reflect their ability.

---

# Young Player

A player is considered young if:

Age <= 21

Rationale:

The age distribution of the dataset shows that players aged 21 or younger represent the younger segment of professional footballers and are therefore suitable for talent identification.

---

# Position Categories

The dataset provides the following position groups:

## Forward

Position contains:

FW

Examples:

* FW
* FW,MF
* MF,FW

---

## Midfielder

Position contains:

MF

Examples:

* MF
* MF,FW
* FW,MF
* DF,MF
* MF,DF

---

## Defender

Position contains:

DF

Examples:

* DF
* DF,MF
* MF,DF

---

## Goalkeeper

Position contains:

GK

---

# Young Talented Forward

A player is classified as a Young Talented Forward if:

* Age <= 21
* Position contains FW
* 90s >= 10
* GoalsPer90 >= 0.398

Rationale:

Young forwards should be evaluated primarily on scoring efficiency rather than total goals.

---

# Young Talented Midfielder

A player is classified as a Young Talented Midfielder if:

* Age <= 21
* Position contains MF
* 90s >= 10
* GoalContributionsPer90 >= 0.496

Rationale:

Midfielders contribute through both goals and assists. Goal contributions provide a more balanced evaluation than assists alone.

---

# Young Talented Defender

A player is classified as a Young Talented Defender if:

* Age <= 21
* Position contains DF
* 90s >= 10
* DefActionsPer90 >= 2.812

Rationale:

Defenders are evaluated based on successful defensive actions rather than attacking statistics.

---

# Young Talented Goalkeeper

A player is classified as a Young Talented Goalkeeper if:

* Age <= 21
* Position contains GK
* 90s >= 3
* Save% >= 76.520

Rationale:

Young goalkeepers typically receive fewer first-team opportunities than outfield players and therefore accumulate fewer playing minutes at an early age. To avoid systematically excluding promising goalkeepers from the talent identification process, a lower minimum playing-time requirement of 3 full matches (90s) is used. Goalkeepers are then evaluated based on their save percentage relative to their peer group.

---

# Hidden Talent

A player is classified as Hidden Talent if:

* Already classified as a Young Talented Player
* Team Standing Rank > 10

Rationale:

Players performing at a high level while playing for lower-ranked teams may receive less attention despite their talent. Such players represent potentially undervalued scouting opportunities.

---

# Knowledge Graph Reasoning Rules

Example reasoning rules:

IF

YoungPlayer
AND
Forward
AND
GoalsPer90 >= 0.398

THEN

YoungTalentedForward

---

IF

YoungTalentedPlayer
AND
StandingsRank > 10

THEN

HiddenTalent

These rules enrich the Knowledge Graph by deriving new knowledge that is not explicitly stored in the original datasets.
