import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE
from runtime import configure_stdout, load_graph

positions = [
    ("YoungTalentedForward", "FORWARDS"),
    ("YoungTalentedMidfielder", "MIDFIELDERS"),
    ("YoungTalentedDefender", "DEFENDERS"),
    ("YoungTalentedGoalkeeper", "GOALKEEPERS"),
]


def main() -> None:
    configure_stdout()
    graph = load_graph(GRAPH_FILE)

    for class_name, label in positions:
        query = f"""
        PREFIX kg: <http://example.org/football-talent-kg/>

        SELECT ?name ?team ?league
        WHERE {{
            ?player a kg:{class_name} .
            ?player kg:hasName ?name .
            ?player kg:playsFor ?teamNode .
            ?teamNode kg:hasName ?team .
            ?teamNode kg:playsInLeague ?leagueNode .
            ?leagueNode kg:hasName ?league .
        }}
        ORDER BY ?league ?team ?name
        """

        results = graph.query(query)

        print(f"\n===== TALENTED {label} =====")

        for row in results:
            print(f"{row.name} | {row.team} | {row.league}")


if __name__ == "__main__":
    main()
