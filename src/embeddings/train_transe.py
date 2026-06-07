import json
import os
import sys
from pathlib import Path

import torch

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import (
    KGE_ENTITY_EMBEDDINGS_FILE,
    KGE_ENTITY_TO_ID_FILE,
    KGE_OUTPUT_DIR,
    KGE_RELATION_TO_ID_FILE,
    KGE_TRIPLES_FILE,
)

os.environ.setdefault("PYSTOW_HOME", str(KGE_OUTPUT_DIR / "pystow"))

from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory


def train_transe():
    KGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not KGE_TRIPLES_FILE.exists():
        raise FileNotFoundError(
            f"Missing triples file: {KGE_TRIPLES_FILE}\n"
            "Run export_triples.py first."
        )

    triples_factory = TriplesFactory.from_path(
        KGE_TRIPLES_FILE,
        create_inverse_triples=False,
    )

    training_tf, testing_tf, validation_tf = triples_factory.split(
        ratios=[0.8, 0.1, 0.1],
        random_state=42,
    )

    result = pipeline(
        training=training_tf,
        testing=testing_tf,
        validation=validation_tf,
        model="TransE",
        training_kwargs={
            "num_epochs": 200,
            "use_tqdm_batch": False,
        },
        random_seed=42,
    )

    result.save_to_directory(KGE_OUTPUT_DIR)

    entity_embeddings = (
        result.model.entity_representations[0](indices=None)
        .detach()
        .cpu()
    )

    torch.save(entity_embeddings, KGE_ENTITY_EMBEDDINGS_FILE)

    with KGE_ENTITY_TO_ID_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            training_tf.entity_to_id,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

    with KGE_RELATION_TO_ID_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            training_tf.relation_to_id,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

    print("TransE training completed successfully")
    print(f"Artifacts: {KGE_OUTPUT_DIR}")
    print(f"Entities: {training_tf.num_entities}")
    print(f"Relations: {training_tf.num_relations}")
    print(f"Embedding shape: {tuple(entity_embeddings.shape)}")


if __name__ == "__main__":
    train_transe()
