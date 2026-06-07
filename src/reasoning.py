import sys
from pathlib import Path

from rdflib import Graph, Namespace, RDF, Literal
from rdflib.namespace import XSD

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE

KG = Namespace("http://example.org/football-talent-kg/")

# Thresholds calculated using calculate_thresholds.py
#
# Forward:
#   GoalsPer90 >= 85th percentile of young forwards
#
# Midfielder:
#   GoalContributionsPer90 >= 85th percentile of young midfielders
#
# Defender:
#   DefActionsPer90 >= 85th percentile of young defenders
#
# Goalkeeper:
#   Save% >= 85th percentile of young goalkeepers
#   (using a lower minimum playing-time requirement of 3 full matches)
FW_THRESHOLD = 0.398
MF_THRESHOLD = 0.496
DF_THRESHOLD = 2.812
GK_THRESHOLD = 76.52

# Minimum playing-time requirements
#
# Outfield players need at least 10 full matches.
# Goalkeepers need at least 3 full matches because young goalkeepers
# generally accumulate fewer first-team minutes.
MIN_90S = 10
GK_MIN_90S = 3
MAX_YOUNG_AGE = 21
HIDDEN_TEAM_RANK = 10


def get_float(graph, subject, predicate):
    value = graph.value(subject, predicate)

    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def get_team_rank(graph, player):
    team = graph.value(player, KG.playsFor)

    if team is None:
        return None

    rank = graph.value(team, KG.hasStandingRank)

    if rank is None:
        return None

    try:
        return int(rank)
    except ValueError:
        return None


def has_position(graph, player, position):
    return (player, KG.hasPosition, position) in graph


def run_reasoning():
    graph = Graph()
    graph.parse(GRAPH_FILE, format="turtle")

    young_players = 0
    talented_forwards = 0
    talented_midfielders = 0
    talented_defenders = 0
    talented_goalkeepers = 0
    hidden_talents = 0

    players = set(graph.subjects(RDF.type, KG.Player))

    for player in players:
        age = get_float(graph, player, KG.hasAge)
        minutes90s = get_float(graph, player, KG.hasMinutes90s)

        if age is None or minutes90s is None:
            continue

        if age <= MAX_YOUNG_AGE:
            graph.add((player, RDF.type, KG.YoungPlayer))
            young_players += 1

        if age > MAX_YOUNG_AGE:
            continue

        is_talented = False

        goals_per90 = get_float(graph, player, KG.hasGoalsPer90)
        goal_contributions_per90 = get_float(
            graph,
            player,
            KG.hasGoalContributionsPer90,
        )
        def_actions_per90 = get_float(
            graph,
            player,
            KG.hasDefActionsPer90,
        )
        save_percentage = get_float(
            graph,
            player,
            KG.hasSavePercentage,
        )

        if (
            has_position(graph, player, KG.Forward)
            and minutes90s >= MIN_90S
            and goals_per90 is not None
            and goals_per90 >= FW_THRESHOLD
        ):
            graph.add((player, RDF.type, KG.YoungTalentedForward))
            graph.add((player, RDF.type, KG.YoungTalentedPlayer))
            talented_forwards += 1
            is_talented = True

        if (
            has_position(graph, player, KG.Midfielder)
            and minutes90s >= MIN_90S
            and goal_contributions_per90 is not None
            and goal_contributions_per90 >= MF_THRESHOLD
        ):
            graph.add((player, RDF.type, KG.YoungTalentedMidfielder))
            graph.add((player, RDF.type, KG.YoungTalentedPlayer))
            talented_midfielders += 1
            is_talented = True

        if (
            has_position(graph, player, KG.Defender)
            and minutes90s >= MIN_90S
            and def_actions_per90 is not None
            and def_actions_per90 >= DF_THRESHOLD
        ):
            graph.add((player, RDF.type, KG.YoungTalentedDefender))
            graph.add((player, RDF.type, KG.YoungTalentedPlayer))
            talented_defenders += 1
            is_talented = True

        if (
            has_position(graph, player, KG.Goalkeeper)
            and minutes90s >= GK_MIN_90S
            and save_percentage is not None
            and save_percentage >= GK_THRESHOLD
        ):
            graph.add((player, RDF.type, KG.YoungTalentedGoalkeeper))
            graph.add((player, RDF.type, KG.YoungTalentedPlayer))
            talented_goalkeepers += 1
            is_talented = True

        team_rank = get_team_rank(graph, player)

        if (
            is_talented
            and team_rank is not None
            and team_rank > HIDDEN_TEAM_RANK
        ):
            graph.add((player, RDF.type, KG.HiddenTalent))
            hidden_talents += 1

    graph.serialize(GRAPH_FILE, format="turtle")

    print("Reasoning completed successfully")
    print(f"Young players: {young_players}")
    print(f"Young talented forwards: {talented_forwards}")
    print(f"Young talented midfielders: {talented_midfielders}")
    print(f"Young talented defenders: {talented_defenders}")
    print(f"Young talented goalkeepers: {talented_goalkeepers}")
    print(f"Hidden talents: {hidden_talents}")


if __name__ == "__main__":
    run_reasoning()
