import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROCESSED_FILE

df = pd.read_csv(PROCESSED_FILE, encoding="utf-8")

print("\n========================")
print("DATASET OVERVIEW")
print("========================")

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns:")
for col in df.columns:
    print(col)

# ----------------------------
# Basic statistics
# ----------------------------

interesting_columns = [
    "Age",
    "90s",
    "Gls",
    "Ast",
    "TklW",
    "Int",
    "Save%",
    "StandingsRk"
]

for column in interesting_columns:
    print(f"\n===== {column} =====")
    print(df[column].describe())

# ----------------------------
# Position distribution
# ----------------------------

print("\n========================")
print("POSITION DISTRIBUTION")
print("========================")

print(df["Pos"].value_counts().head(20))

# ----------------------------
# Age distribution
# ----------------------------

print("\n========================")
print("AGE DISTRIBUTION")
print("========================")

print(df["Age"].value_counts().sort_index())

# ----------------------------
# Top scorers
# ----------------------------

print("\n========================")
print("TOP GOAL SCORERS")
print("========================")

print(
    df[["Player", "Squad", "Age", "Gls"]]
    .sort_values("Gls", ascending=False)
    .head(20)
)

# ----------------------------
# Top assist providers
# ----------------------------

print("\n========================")
print("TOP ASSISTS")
print("========================")

print(
    df[["Player", "Squad", "Age", "Ast"]]
    .sort_values("Ast", ascending=False)
    .head(20)
)

# ----------------------------
# Best defenders
# ----------------------------

df["DefActions"] = df["TklW"].fillna(0) + df["Int"].fillna(0)

print("\n========================")
print("TOP DEFENSIVE ACTIONS")
print("========================")

print(
    df[["Player", "Squad", "Age", "DefActions"]]
    .sort_values("DefActions", ascending=False)
    .head(20)
)

# ----------------------------
# Goalkeepers
# ----------------------------

gks = df[df["Pos"].str.contains("GK", na=False)]

print("\n========================")
print("TOP GOALKEEPERS")
print("========================")

print(
    gks[["Player", "Squad", "Age", "Save%"]]
    .sort_values("Save%", ascending=False)
    .head(20)
)
