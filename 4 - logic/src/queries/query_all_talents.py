import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE
from runtime import configure_stdout, load_graph

QUERY = """
PREFIX kg: <http://example.org/football-talent-kg/>

SELECT DISTINCT ?name ?team ?league ?position
WHERE {
    ?player a kg:YoungTalentedPlayer .
    ?player kg:hasName ?name .
    ?player kg:playsFor ?teamNode .
    ?teamNode kg:hasName ?team .
    ?teamNode kg:playsInLeague ?leagueNode .
    ?leagueNode kg:hasName ?league .
    ?player kg:hasPosition ?positionNode .
    BIND(STRAFTER(STR(?positionNode), "http://example.org/football-talent-kg/") AS ?position)
}
ORDER BY ?league ?team ?name ?position
"""


def main() -> None:
    configure_stdout()
    graph = load_graph(GRAPH_FILE)
    results = graph.query(QUERY)

    print("===== ALL TALENTS =====")

    for row in results:
        print(f"{row.name} | {row.position} | {row.team} | {row.league}")


if __name__ == "__main__":
    main()
