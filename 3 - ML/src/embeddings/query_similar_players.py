import json
import sys
import unicodedata
from pathlib import Path
from difflib import get_close_matches

import torch
import torch.nn.functional as F
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import (
    GRAPH_FILE,
    KGE_ENTITY_EMBEDDINGS_FILE,
    KGE_ENTITY_TO_ID_FILE,
)

KG = Namespace("http://example.org/football-talent-kg/")


def normalize_player_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(
        char
        for char in normalized
        if not unicodedata.combining(char)
    )
    return " ".join(normalized.casefold().split())


def load_player_lookup(graph):
    lookup = {}
    entity_to_name = {}

    for player in set(graph.subjects(RDF.type, KG.Player)):
        name = graph.value(player, KG.hasName)
        if name is None:
            continue

        canonical_name = str(name)
        local_name = str(player).rsplit("/", 1)[-1]
        normalized_name = normalize_player_name(canonical_name)

        lookup[canonical_name] = {
            "entity": local_name,
            "canonical": canonical_name,
        }

        lookup.setdefault(
            normalized_name,
            {
                "entity": local_name,
                "canonical": canonical_name,
            },
        )

        entity_to_name[local_name] = canonical_name

    return lookup, entity_to_name


def get_player_metadata(graph, player_uri):
    team_node = graph.value(player_uri, KG.playsFor)
    team_name = graph.value(team_node, KG.hasName) if team_node else None
    age = graph.value(player_uri, KG.hasAge)

    league_name = None
    if team_node is not None:
        league_node = graph.value(team_node, KG.playsInLeague)
        league_name = graph.value(league_node, KG.hasName) if league_node else None

    positions = sorted(
        {
            str(position).rsplit("/", 1)[-1]
            for position in graph.objects(player_uri, KG.hasPosition)
        }
    )

    return {
        "age": str(age) if age is not None else "Unknown",
        "team": str(team_name) if team_name else "Unknown",
        "league": str(league_name) if league_name else "Unknown",
        "positions": ", ".join(positions) if positions else "Unknown",
    }


def query_similar_players(player_name: str, top_k: int = 5):
    if not KGE_ENTITY_EMBEDDINGS_FILE.exists() or not KGE_ENTITY_TO_ID_FILE.exists():
        raise FileNotFoundError(
            "Missing embedding artifacts.\n"
            "Run export_triples.py and train_transe.py first."
        )

    graph = Graph()
    graph.parse(GRAPH_FILE, format="turtle")

    with KGE_ENTITY_TO_ID_FILE.open("r", encoding="utf-8") as file:
        entity_to_id = json.load(file)

    try:
        embeddings = torch.load(
            KGE_ENTITY_EMBEDDINGS_FILE,
            map_location="cpu",
            weights_only=True,
        )
    except TypeError:
        embeddings = torch.load(
            KGE_ENTITY_EMBEDDINGS_FILE,
            map_location="cpu",
        )

    player_lookup, entity_to_name = load_player_lookup(graph)

    player_info = player_lookup.get(player_name)
    if player_info is None:
        normalized_input = normalize_player_name(player_name)
        player_info = player_lookup.get(normalized_input)

    if player_info is None:
        canonical_names = sorted(
            {
                value["canonical"]
                for key, value in player_lookup.items()
                if key == value["canonical"]
            }
        )
        suggestions = get_close_matches(
            player_name,
            canonical_names,
            n=5,
            cutoff=0.6,
        )
        message = f"Unknown player: {player_name}"
        if suggestions:
            message += f"\nDid you mean: {suggestions}"
        else:
            message += f"\nExample names: {canonical_names[:10]}"
        raise ValueError(message)

    target_entity = player_info["entity"]
    target_name = player_info["canonical"]

    if target_entity not in entity_to_id:
        raise ValueError(
            f"Player entity not found in embeddings: {target_entity}"
        )

    target_id = entity_to_id[target_entity]
    normalized = F.normalize(embeddings, p=2, dim=1)
    scores = torch.matmul(normalized, normalized[target_id])
    scores[target_id] = -1.0

    id_to_entity = {
        entity_id: entity_name
        for entity_name, entity_id in entity_to_id.items()
    }

    player_entities = {
        entity_to_id[value["entity"]]
        for value in player_lookup.values()
        if isinstance(value, dict) and value["entity"] in entity_to_id
    }

    ranked_ids = [
        idx
        for idx in torch.argsort(scores, descending=True).tolist()
        if idx in player_entities
    ][:top_k]

    print(f"===== MOST SIMILAR PLAYERS TO {target_name} =====")

    for rank, entity_id in enumerate(ranked_ids, start=1):
        entity_name = id_to_entity[entity_id]
        similar_name = entity_to_name.get(entity_name, entity_name)
        player_uri = KG[entity_name]
        metadata = get_player_metadata(graph, player_uri)
        similarity = scores[entity_id].item()

        print(
            f"{rank}. {similar_name} | "
            f"Age {metadata['age']} | "
            f"{metadata['positions']} | "
            f"{metadata['team']} | "
            f"{metadata['league']} | "
            f"score={similarity:.4f}"
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(
            'Usage: python query_similar_players.py "Player Name"'
        )

    query_similar_players(sys.argv[1])
