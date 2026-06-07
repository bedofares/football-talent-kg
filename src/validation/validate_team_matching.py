import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

players = pd.read_csv(
    Path(__file__).resolve().parents[2] / "data/raw/kaggle/players_data_light-2025_2026.csv",
    encoding="utf-8",
)

standings = pd.read_csv(
    Path(__file__).resolve().parents[2] / "data/raw/standings.csv",
    encoding="utf-8",
)

player_teams = set(players["Squad"].unique())
standing_teams = set(standings["Squad"].unique())

print("Missing from standings:")
print(sorted(player_teams - standing_teams))

print("\nMissing from players:")
print(sorted(standing_teams - player_teams))
