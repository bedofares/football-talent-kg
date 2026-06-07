import pandas as pd

from config import (
    PLAYERS_FILE,
    STANDINGS_FILE,
    PROCESSED_FILE,
)

LEAGUE_MAP = {
    "eng Premier League": "Premier League",
    "es La Liga": "La Liga",
    "de Bundesliga": "Bundesliga",
    "it Serie A": "Serie A",
    "fr Ligue 1": "Ligue 1",
}


def preprocess():
    print("Loading datasets...")

    players = pd.read_csv(
        PLAYERS_FILE,
        encoding="utf-8"
    )

    standings = pd.read_csv(
        STANDINGS_FILE,
        encoding="utf-8"
    )

    print(f"Players loaded: {len(players)}")
    print(f"Standings loaded: {len(standings)}")

    # =====================================
    # League Normalization
    # =====================================

    players["League"] = players["Comp"].map(
        LEAGUE_MAP
    )

    # =====================================
    # Merge Player Data + Team Standings
    # =====================================

    merged = players.merge(
        standings,
        on=["Squad", "League"],
        how="left",
        suffixes=("_player", "_standing"),
    )

    merged = merged.rename(
        columns={
            "Rk_standing": "StandingsRk"
        }
    )

    # =====================================
    # Feature Engineering
    # =====================================

    print("Creating derived features...")

    minutes_played = merged["90s"].replace(
        0,
        pd.NA
    )

    # Attacking Metrics

    merged["GoalsPer90"] = (
        merged["Gls"] / minutes_played
    )

    merged["AssistsPer90"] = (
        merged["Ast"] / minutes_played
    )

    merged["GoalContributionsPer90"] = (
        (
            merged["Gls"]
            + merged["Ast"]
        )
        / minutes_played
    )

    # Defensive Metrics

    merged["DefActions"] = (
        merged["TklW"].fillna(0)
        + merged["Int"].fillna(0)
    )

    merged["DefActionsPer90"] = (
        merged["DefActions"]
        / minutes_played
    )

    # =====================================
    # Validation
    # =====================================

    print("\nValidation Results")

    print(f"Players: {len(players)}")
    print(f"Merged: {len(merged)}")

    missing_ranks = (
        merged["StandingsRk"]
        .isna()
        .sum()
    )

    print(
        f"Missing ranks: {missing_ranks}"
    )

    # =====================================
    # Save Processed Dataset
    # =====================================

    merged.to_csv(
        PROCESSED_FILE,
        index=False
    )

    print(
        f"\nProcessed file saved to:\n{PROCESSED_FILE}"
    )

    print("\nCreated Features:")
    print("- GoalsPer90")
    print("- AssistsPer90")
    print("- GoalContributionsPer90")
    print("- DefActions")
    print("- DefActionsPer90")


if __name__ == "__main__":
    preprocess()
