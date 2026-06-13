import json
import random
import sys
from pathlib import Path

import pandas as pd
import torch
import torch.nn.functional as F

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


def build_id_map(values):
    return {
        value: index
        for index, value in enumerate(sorted(set(values)))
    }


def make_training_tensor(triples, entity_to_id, relation_to_id):
    rows = [
        (
            entity_to_id[row.head],
            relation_to_id[row.relation],
            entity_to_id[row.tail],
        )
        for row in triples.itertuples(index=False)
    ]
    return torch.tensor(rows, dtype=torch.long)


def train_transe(
    embedding_dim=64,
    num_epochs=200,
    batch_size=512,
    learning_rate=0.01,
    margin=1.0,
    seed=42,
):
    KGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not KGE_TRIPLES_FILE.exists():
        raise FileNotFoundError(
            f"Missing triples file: {KGE_TRIPLES_FILE}\n"
            "Run export_triples.py first."
        )

    random.seed(seed)
    torch.manual_seed(seed)

    triples = pd.read_csv(KGE_TRIPLES_FILE, sep="\t")

    entity_to_id = build_id_map(
        list(triples["head"]) + list(triples["tail"])
    )
    relation_to_id = build_id_map(triples["relation"])

    training = make_training_tensor(
        triples,
        entity_to_id,
        relation_to_id,
    )

    num_entities = len(entity_to_id)
    num_relations = len(relation_to_id)

    entity_embeddings = torch.nn.Embedding(num_entities, embedding_dim)
    relation_embeddings = torch.nn.Embedding(num_relations, embedding_dim)

    torch.nn.init.xavier_uniform_(entity_embeddings.weight)
    torch.nn.init.xavier_uniform_(relation_embeddings.weight)

    optimizer = torch.optim.Adam(
        list(entity_embeddings.parameters())
        + list(relation_embeddings.parameters()),
        lr=learning_rate,
    )

    for epoch in range(num_epochs):
        permutation = torch.randperm(training.shape[0])
        epoch_loss = 0.0

        for start in range(0, training.shape[0], batch_size):
            batch_ids = permutation[start:start + batch_size]
            positive = training[batch_ids]
            negative = positive.clone()
            negative[:, 2] = torch.randint(
                0,
                num_entities,
                (negative.shape[0],),
            )

            positive_score = torch.linalg.vector_norm(
                entity_embeddings(positive[:, 0])
                + relation_embeddings(positive[:, 1])
                - entity_embeddings(positive[:, 2]),
                ord=1,
                dim=1,
            )
            negative_score = torch.linalg.vector_norm(
                entity_embeddings(negative[:, 0])
                + relation_embeddings(negative[:, 1])
                - entity_embeddings(negative[:, 2]),
                ord=1,
                dim=1,
            )

            loss = F.relu(margin + positive_score - negative_score).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            with torch.no_grad():
                entity_embeddings.weight[:] = F.normalize(
                    entity_embeddings.weight,
                    p=2,
                    dim=1,
                )

            epoch_loss += loss.item()

        if (epoch + 1) % 50 == 0:
            print(
                f"Epoch {epoch + 1}/{num_epochs} "
                f"loss={epoch_loss:.4f}"
            )

    final_entity_embeddings = (
        entity_embeddings.weight
        .detach()
        .cpu()
    )

    torch.save(final_entity_embeddings, KGE_ENTITY_EMBEDDINGS_FILE)

    with KGE_ENTITY_TO_ID_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            entity_to_id,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

    with KGE_RELATION_TO_ID_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            relation_to_id,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

    print("TransE training completed successfully")
    print(f"Artifacts: {KGE_OUTPUT_DIR}")
    print(f"Entities: {num_entities}")
    print(f"Relations: {num_relations}")
    print(f"Embedding shape: {tuple(final_entity_embeddings.shape)}")


if __name__ == "__main__":
    train_transe()
