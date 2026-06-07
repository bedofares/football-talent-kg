from ScraperFC.fbref import FBref

fbref = FBref()

stats = fbref.scrape_stats(
    year="2025-2026",
    league="England Premier League",
    stat_category="standard"
)

print("Available tables:")
print(stats.keys())

print("\nPLAYER TABLE COLUMNS:")
print(stats["player"].columns.tolist())

print("\nFIRST 5 ROWS:")
print(stats["player"].head())