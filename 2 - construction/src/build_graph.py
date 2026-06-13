import math
import re

import pandas as pd
from rdflib import Graph, Namespace, RDF, RDFS, Literal, XSD

from config import PROCESSED_FILE, GRAPH_FILE, OUTPUT_DIR

KG = Namespace("http://example.org/football-talent-kg/")


def make_uri(value: str):
    clean = str(value).strip()
    clean = re.sub(r"[^a-zA-Z0-9]+", "_", clean)
    clean = clean.strip("_")
    return KG[clean]


def add_literal_if_valid(graph, subject, predicate, value, datatype=None):
    if value is None:
        return

    if isinstance(value, float) and math.isnan(value):
        return

    graph.add(
        (
            subject,
            predicate,
            Literal(value, datatype=datatype),
        )
    )


def get_positions(pos_value: str):
    positions = []

    pos_value = str(pos_value)

    if "FW" in pos_value:
        positions.append("Forward")

    if "MF" in pos_value:
        positions.append("Midfielder")

    if "DF" in pos_value:
        positions.append("Defender")

    if "GK" in pos_value:
        positions.append("Goalkeeper")

    return positions


def build_graph():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Loading processed dataset...")

    df = pd.read_csv(
        PROCESSED_FILE,
        encoding="utf-8",
    )

    original_rows = len(df)

    # Keep the club where the player accumulated
    # the most playing time during the season
    df = (
        df.sort_values(
            "90s",
            ascending=False,
        )
        .drop_duplicates(
            subset=["Player"],
            keep="first",
        )
    )

    print(
        f"Removed {original_rows - len(df)} duplicate player rows"
    )

    print(
        f"Players used in graph: {len(df)}"
    )

    graph = Graph()

    graph.bind("kg", KG)
    graph.bind("rdfs", RDFS)

    # ==========================================
    # Classes
    # ==========================================

    classes = [
        "Player",
        "Team",
        "League",
        "Position",
        "Forward",
        "Midfielder",
        "Defender",
        "Goalkeeper",
        "YoungPlayer",
        "YoungTalentedPlayer",
        "YoungTalentedForward",
        "YoungTalentedMidfielder",
        "YoungTalentedDefender",
        "YoungTalentedGoalkeeper",
        "HiddenTalent",
    ]

    for class_name in classes:
        graph.add(
            (
                KG[class_name],
                RDF.type,
                RDFS.Class,
            )
        )

    # ==========================================
    # Position hierarchy
    # ==========================================

    for position in [
        "Forward",
        "Midfielder",
        "Defender",
        "Goalkeeper",
    ]:
        graph.add(
            (
                KG[position],
                RDFS.subClassOf,
                KG.Position,
            )
        )

    # ==========================================
    # Talent hierarchy
    # ==========================================

    graph.add(
        (
            KG.YoungPlayer,
            RDFS.subClassOf,
            KG.Player,
        )
    )

    graph.add(
        (
            KG.YoungTalentedPlayer,
            RDFS.subClassOf,
            KG.YoungPlayer,
        )
    )

    graph.add(
        (
            KG.YoungTalentedForward,
            RDFS.subClassOf,
            KG.YoungTalentedPlayer,
        )
    )

    graph.add(
        (
            KG.YoungTalentedMidfielder,
            RDFS.subClassOf,
            KG.YoungTalentedPlayer,
        )
    )

    graph.add(
        (
            KG.YoungTalentedDefender,
            RDFS.subClassOf,
            KG.YoungTalentedPlayer,
        )
    )

    graph.add(
        (
            KG.YoungTalentedGoalkeeper,
            RDFS.subClassOf,
            KG.YoungTalentedPlayer,
        )
    )

    graph.add(
        (
            KG.HiddenTalent,
            RDFS.subClassOf,
            KG.YoungTalentedPlayer,
        )
    )

    # ==========================================
    # Instances
    # ==========================================

    for _, row in df.iterrows():
        player = make_uri(row["Player"])
        team = make_uri(row["Squad"])
        league = make_uri(row["League"])

        # Types

        graph.add((player, RDF.type, KG.Player))
        graph.add((team, RDF.type, KG.Team))
        graph.add((league, RDF.type, KG.League))

        # Relationships

        graph.add((player, KG.playsFor, team))
        graph.add((team, KG.playsInLeague, league))

        # Player literals

        add_literal_if_valid(
            graph,
            player,
            KG.hasName,
            row["Player"],
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasAge,
            row["Age"],
            XSD.float,
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasNation,
            row["Nation"],
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasMinutes90s,
            row["90s"],
            XSD.float,
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasGoalsPer90,
            row["GoalsPer90"],
            XSD.float,
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasAssistsPer90,
            row["AssistsPer90"],
            XSD.float,
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasGoalContributionsPer90,
            row["GoalContributionsPer90"],
            XSD.float,
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasDefActionsPer90,
            row["DefActionsPer90"],
            XSD.float,
        )

        add_literal_if_valid(
            graph,
            player,
            KG.hasSavePercentage,
            row["Save%"],
            XSD.float,
        )

        # Team literals

        add_literal_if_valid(
            graph,
            team,
            KG.hasName,
            row["Squad"],
        )

        add_literal_if_valid(
            graph,
            team,
            KG.hasStandingRank,
            row["StandingsRk"],
            XSD.integer,
        )

        # League literals

        add_literal_if_valid(
            graph,
            league,
            KG.hasName,
            row["League"],
        )

        # Positions

        for position_name in get_positions(row["Pos"]):
            graph.add(
                (
                    player,
                    KG.hasPosition,
                    KG[position_name],
                )
            )

    graph.serialize(
        destination=GRAPH_FILE,
        format="turtle",
    )

    print("\nKnowledge Graph created successfully")
    print(f"Output: {GRAPH_FILE}")
    print(f"Triples: {len(graph)}")


if __name__ == "__main__":
    build_graph()