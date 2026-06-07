import sys
from pathlib import Path

import pandas as pd
from ScraperFC.fbref import FBref

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import STANDINGS_FILE

LEAGUES = {
    "Premier League": "England Premier League",
    "La Liga": "Spain La Liga",
    "Bundesliga": "Germany Bundesliga",
    "Serie A": "Italy Serie A",
    "Ligue 1": "France Ligue 1",
}


def main() -> None:
    fbref = FBref()
    all_tables = []

    for league_name, fbref_name in LEAGUES.items():
        table = fbref.scrape_league_table(
            year="2025-2026",
            league=fbref_name,
        )[0]
        table["League"] = league_name
        all_tables.append(table[["Rk", "Squad", "League"]])

    standings = pd.concat(all_tables)
    standings.to_csv(STANDINGS_FILE, index=False)
    print("standings.csv created successfully")


if __name__ == "__main__":
    main()
