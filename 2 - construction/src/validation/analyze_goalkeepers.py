import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROCESSED_FILE
from runtime import configure_stdout


def main() -> None:
    configure_stdout()
    df = pd.read_csv(PROCESSED_FILE)

    young_gks = df[
        (df["Pos"].str.contains("GK", na=False))
        & (df["Age"] <= 21)
    ]

    print(f"Young GKs: {len(young_gks)}")
    print(
        young_gks[
            ["Player", "Age", "90s", "Save%"]
        ]
        .sort_values("Save%", ascending=False)
        .head(20)
    )


if __name__ == "__main__":
    main()
