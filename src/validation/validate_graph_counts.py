import sys
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import GRAPH_FILE

KG = Namespace(
    "http://example.org/football-talent-kg/"
)

graph = Graph()
graph.parse(GRAPH_FILE, format="turtle")

def count_instances(class_name):
    return len(set(graph.subjects(RDF.type, KG[class_name])))


players = count_instances("Player")
teams = count_instances("Team")
leagues = count_instances("League")
young_players = count_instances("YoungPlayer")
talented_forwards = count_instances("YoungTalentedForward")
talented_midfielders = count_instances("YoungTalentedMidfielder")
talented_defenders = count_instances("YoungTalentedDefender")
talented_goalkeepers = count_instances("YoungTalentedGoalkeeper")
hidden_talents = count_instances("HiddenTalent")

print(f"Players: {players}")
print(f"Teams: {teams}")
print(f"Leagues: {leagues}")
print(f"Young players: {young_players}")
print(f"Young talented forwards: {talented_forwards}")
print(f"Young talented midfielders: {talented_midfielders}")
print(f"Young talented defenders: {talented_defenders}")
print(f"Young talented goalkeepers: {talented_goalkeepers}")
print(f"Hidden talents: {hidden_talents}")
print(f"Triples: {len(graph)}")
