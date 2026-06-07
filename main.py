import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
EMBEDDINGS_DIR = SRC_DIR / "embeddings"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(EMBEDDINGS_DIR) not in sys.path:
    sys.path.insert(0, str(EMBEDDINGS_DIR))

from build_graph import build_graph
from preprocess import preprocess
from reasoning import run_reasoning


def run_pipeline():
    print("Running full football talent pipeline...")
    preprocess()
    build_graph()
    run_reasoning()
    print("Pipeline completed successfully.")


def run_embeddings_pipeline():
    from export_triples import export_triples
    from train_transe import train_transe

    print("Running embeddings pipeline...")
    export_triples()
    train_transe()
    print("Embeddings pipeline completed successfully.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the football talent knowledge graph pipeline.",
    )
    parser.add_argument(
        "step",
        nargs="?",
        default="all",
        choices=[
            "all",
            "preprocess",
            "build-graph",
            "reasoning",
            "embeddings",
            "all-with-embeddings",
            "similar-players",
        ],
        help="Pipeline step to run. Defaults to the full pipeline.",
    )
    parser.add_argument(
        "player_name",
        nargs="?",
        help='Player name for "similar-players".',
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.step == "all":
        run_pipeline()
    elif args.step == "preprocess":
        preprocess()
    elif args.step == "build-graph":
        build_graph()
    elif args.step == "reasoning":
        run_reasoning()
    elif args.step == "embeddings":
        run_embeddings_pipeline()
    elif args.step == "all-with-embeddings":
        run_pipeline()
        run_embeddings_pipeline()
    elif args.step == "similar-players":
        from query_similar_players import query_similar_players

        if not args.player_name:
            raise SystemExit(
                'Usage: python main.py similar-players "Player Name"'
            )
        query_similar_players(args.player_name)


if __name__ == "__main__":
    main()
