import sys
from pathlib import Path

import pandas as pd
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE, KGE_TRIPLES_FILE

KG = Namespace("http://example.org/football-talent-kg/")

ALLOWED_TYPE_OBJECTS = {
    KG.Player,
    KG.Team,
    KG.League,
    KG.Forward,
    KG.Midfielder,
    KG.Defender,
    KG.Goalkeeper,
    KG.YoungPlayer,
    KG.YoungTalentedPlayer,
    KG.YoungTalentedForward,
    KG.YoungTalentedMidfielder,
    KG.YoungTalentedDefender,
    KG.YoungTalentedGoalkeeper,
    KG.HiddenTalent,
}

ALLOWED_RELATIONS = {
    KG.playsFor,
    KG.playsInLeague,
    KG.hasPosition,
}


def local_name(uri) -> str:
    value = str(uri)
    return value.rsplit("/", 1)[-1]


def export_triples():
    graph = Graph()
    graph.parse(GRAPH_FILE, format="turtle")

    rows = []

    for subject, predicate, obj in graph:
        if predicate == RDF.type:
            if obj in ALLOWED_TYPE_OBJECTS:
                rows.append(
                    {
                        "head": local_name(subject),
                        "relation": "type",
                        "tail": local_name(obj),
                    }
                )
            continue

        if predicate in ALLOWED_RELATIONS:
            rows.append(
                {
                    "head": local_name(subject),
                    "relation": local_name(predicate),
                    "tail": local_name(obj),
                }
            )

    triples = (
        pd.DataFrame(rows)
        .drop_duplicates()
        .sort_values(["relation", "head", "tail"])
        .reset_index(drop=True)
    )

    KGE_TRIPLES_FILE.parent.mkdir(parents=True, exist_ok=True)
    triples.to_csv(KGE_TRIPLES_FILE, sep="\t", index=False)

    print("KGE triples exported successfully")
    print(f"Output: {KGE_TRIPLES_FILE}")
    print(f"Triples: {len(triples)}")
    print("\nRelations included:")
    for relation in sorted(triples["relation"].unique()):
        print(f"- {relation}")


if __name__ == "__main__":
    export_triples()
