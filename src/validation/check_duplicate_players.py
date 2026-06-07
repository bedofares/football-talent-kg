import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROCESSED_FILE


def main() -> None:
    df = pd.read_csv(PROCESSED_FILE)
    duplicates = (
        df.groupby("Player")
        .size()
        .reset_index(name="Count")
    )

    duplicates = duplicates[
        duplicates["Count"] > 1
    ]

    print(f"Players with multiple rows: {len(duplicates)}")
    print("\nTop examples:\n")
    print(
        duplicates.sort_values(
            "Count",
            ascending=False
        ).head(20)
    )


if __name__ == "__main__":
    main()
