import sys
from pathlib import Path

from rdflib import Graph

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE

graph = Graph()
graph.parse(GRAPH_FILE, format="turtle")

query = """
PREFIX kg: <http://example.org/football-talent-kg/>

SELECT DISTINCT ?league ?name ?position ?team
WHERE {
    ?player a kg:HiddenTalent .
    ?player kg:hasName ?name .
    ?player kg:hasPosition ?positionNode .
    BIND(STRAFTER(STR(?positionNode), "http://example.org/football-talent-kg/") AS ?position)
    ?player kg:playsFor ?teamNode .
    ?teamNode kg:hasName ?team .
    ?teamNode kg:playsInLeague ?leagueNode .
    ?leagueNode kg:hasName ?league .
}
ORDER BY ?league ?team ?name ?position
"""

results = graph.query(query)

print("===== HIDDEN TALENTS BY LEAGUE =====")

current_league = None

for row in results:
    if row.league != current_league:
        current_league = row.league
        print(f"\n{current_league}")

    print(f"{row.name} | {row.position} | {row.team}")
