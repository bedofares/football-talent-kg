import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PLAYERS_FILE, STANDINGS_FILE


def main() -> None:
    players = pd.read_csv(
        PLAYERS_FILE,
        encoding="utf-8",
    )
    standings = pd.read_csv(
        STANDINGS_FILE,
        encoding="utf-8",
    )

    player_teams = set(players["Squad"].unique())
    standing_teams = set(standings["Squad"].unique())

    print("Missing from standings:")
    print(sorted(player_teams - standing_teams))

    print("\nMissing from players:")
    print(sorted(standing_teams - player_teams))


if __name__ == "__main__":
    main()
