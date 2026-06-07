import sys
from pathlib import Path

from rdflib import Graph, Namespace, RDF

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE

KG = Namespace("http://example.org/football-talent-kg/")

graph = Graph()
graph.parse(GRAPH_FILE, format="turtle")


def print_players(class_name):
    print(f"\n===== {class_name} =====")

    players = set(
        graph.subjects(
            RDF.type,
            KG[class_name]
        )
    )

    print(f"Count: {len(players)}")

    for player in sorted(players)[:20]:
        name = graph.value(
            player,
            KG.hasName
        )
        print(name)


print_players("YoungTalentedForward")
print_players("YoungTalentedMidfielder")
print_players("YoungTalentedDefender")
print_players("YoungTalentedGoalkeeper")
print_players("HiddenTalent")
