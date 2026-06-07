from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ==========================
# Raw Data
# ==========================

PLAYERS_FILE = (
    ROOT / "data/raw/kaggle/players_data_light-2025_2026.csv"
)

STANDINGS_FILE = (
    ROOT / "data/raw/standings.csv"
)

# ==========================
# Processed Data
# ==========================

PROCESSED_FILE = (
    ROOT / "data/processed/players_with_standings.csv"
)

# ==========================
# Output Files
# ==========================

OUTPUT_DIR = (
    ROOT / "output"
)

GRAPH_FILE = (
    OUTPUT_DIR / "football_talent_kg.ttl"
)

KGE_OUTPUT_DIR = (
    OUTPUT_DIR / "transe_model"
)

KGE_TRIPLES_FILE = (
    ROOT / "data/processed/kg_triples.tsv"
)

KGE_ENTITY_EMBEDDINGS_FILE = (
    KGE_OUTPUT_DIR / "entity_embeddings.pt"
)

KGE_ENTITY_TO_ID_FILE = (
    KGE_OUTPUT_DIR / "entity_to_id.json"
)

KGE_RELATION_TO_ID_FILE = (
    KGE_OUTPUT_DIR / "relation_to_id.json"
)

# ==========================
# Documentation
# ==========================

DOCS_DIR = (
    ROOT / "docs"
)

RULES_FILE = (
    DOCS_DIR / "rules.md"
)

ONTOLOGY_FILE = (
    DOCS_DIR / "ontology.md"
)

KGE_DOC_FILE = (
    DOCS_DIR / "kg_embeddings.md"
)
