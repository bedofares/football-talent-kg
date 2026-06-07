import sys
from pathlib import Path

from rdflib import Namespace, RDF

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE
from runtime import configure_stdout, load_graph

KG = Namespace("http://example.org/football-talent-kg/")


def print_players(graph, class_name) -> None:
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


def main() -> None:
    configure_stdout()
    graph = load_graph(GRAPH_FILE)
    print_players(graph, "YoungTalentedForward")
    print_players(graph, "YoungTalentedMidfielder")
    print_players(graph, "YoungTalentedDefender")
    print_players(graph, "YoungTalentedGoalkeeper")
    print_players(graph, "HiddenTalent")


if __name__ == "__main__":
    main()
