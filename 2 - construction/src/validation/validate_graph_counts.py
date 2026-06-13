import sys
from pathlib import Path

from rdflib import Namespace
from rdflib.namespace import RDF

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE
from runtime import load_graph

KG = Namespace(
    "http://example.org/football-talent-kg/"
)


def count_instances(graph, class_name) -> int:
    return len(set(graph.subjects(RDF.type, KG[class_name])))


def main() -> None:
    graph = load_graph(GRAPH_FILE)
    print(f"Players: {count_instances(graph, 'Player')}")
    print(f"Teams: {count_instances(graph, 'Team')}")
    print(f"Leagues: {count_instances(graph, 'League')}")
    print(f"Young players: {count_instances(graph, 'YoungPlayer')}")
    print(
        "Young talented forwards: "
        f"{count_instances(graph, 'YoungTalentedForward')}"
    )
    print(
        "Young talented midfielders: "
        f"{count_instances(graph, 'YoungTalentedMidfielder')}"
    )
    print(
        "Young talented defenders: "
        f"{count_instances(graph, 'YoungTalentedDefender')}"
    )
    print(
        "Young talented goalkeepers: "
        f"{count_instances(graph, 'YoungTalentedGoalkeeper')}"
    )
    print(f"Hidden talents: {count_instances(graph, 'HiddenTalent')}")
    print(f"Triples: {len(graph)}")


if __name__ == "__main__":
    main()
