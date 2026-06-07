import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROCESSED_FILE

INTERESTING_COLUMNS = [
    "Age",
    "90s",
    "Gls",
    "Ast",
    "TklW",
    "Int",
    "Save%",
    "StandingsRk",
]


def main() -> None:
    df = pd.read_csv(PROCESSED_FILE, encoding="utf-8")

    print("\n========================")
    print("DATASET OVERVIEW")
    print("========================")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(column)

    for column in INTERESTING_COLUMNS:
        print(f"\n===== {column} =====")
        print(df[column].describe())

    print("\n========================")
    print("POSITION DISTRIBUTION")
    print("========================")
    print(df["Pos"].value_counts().head(20))

    print("\n========================")
    print("AGE DISTRIBUTION")
    print("========================")
    print(df["Age"].value_counts().sort_index())

    print("\n========================")
    print("TOP GOAL SCORERS")
    print("========================")
    print(
        df[["Player", "Squad", "Age", "Gls"]]
        .sort_values("Gls", ascending=False)
        .head(20)
    )

    print("\n========================")
    print("TOP ASSISTS")
    print("========================")
    print(
        df[["Player", "Squad", "Age", "Ast"]]
        .sort_values("Ast", ascending=False)
        .head(20)
    )

    df["DefActions"] = df["TklW"].fillna(0) + df["Int"].fillna(0)

    print("\n========================")
    print("TOP DEFENSIVE ACTIONS")
    print("========================")
    print(
        df[["Player", "Squad", "Age", "DefActions"]]
        .sort_values("DefActions", ascending=False)
        .head(20)
    )

    gks = df[df["Pos"].str.contains("GK", na=False)]

    print("\n========================")
    print("TOP GOALKEEPERS")
    print("========================")
    print(
        gks[["Player", "Squad", "Age", "Save%"]]
        .sort_values("Save%", ascending=False)
        .head(20)
    )


if __name__ == "__main__":
    main()
