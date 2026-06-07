from ScraperFC.fbref import FBref
import pandas as pd

fbref = FBref()

leagues = {
    "Premier League": "England Premier League",
    "La Liga": "Spain La Liga",
    "Bundesliga": "Germany Bundesliga",
    "Serie A": "Italy Serie A",
    "Ligue 1": "France Ligue 1"
}

all_tables = []

for league_name, fbref_name in leagues.items():
    table = fbref.scrape_league_table(
        year="2025-2026",
        league=fbref_name
    )[0]

    table["League"] = league_name

    all_tables.append(
        table[["Rk", "Squad", "League"]]
    )

standings = pd.concat(all_tables)

standings.to_csv(
    "data/raw/standings.csv",
    index=False
)

print("standings.csv created successfully")