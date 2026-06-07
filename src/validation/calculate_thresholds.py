import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROCESSED_FILE

MIN_90S = 10
GK_MIN_90S = 3
MAX_YOUNG_AGE = 21

df = pd.read_csv(PROCESSED_FILE)

# Talent identification thresholds
#
# Thresholds are calculated from:
# - Young players (Age <= 21)
# - Players with sufficient playing time
#
# Outfield players:
# - Minimum 10 full matches (90s)
# - 85th percentile threshold
#
# Goalkeepers:
# - Minimum 3 full matches (90s)
# - 85th percentile threshold
#
# A lower playing-time requirement is used for goalkeepers because
# young goalkeepers typically receive fewer first-team opportunities
# than outfield players.

eligible = df[
    (df["90s"] >= MIN_90S)
    & (df["Age"] <= MAX_YOUNG_AGE)
]
print(f"Eligible outfield pool: {len(eligible)}")

# ---------------------------------
# Forwards
# ---------------------------------

fw = eligible[
    eligible["Pos"].str.contains("FW", na=False)
]

fw_threshold = fw["GoalsPer90"].quantile(0.85)

# ---------------------------------
# Midfielders
# ---------------------------------

mf = eligible[
    eligible["Pos"].str.contains("MF", na=False)
]

mf_threshold = (
    mf["GoalContributionsPer90"]
    .quantile(0.85)
)

# ---------------------------------
# Defenders
# ---------------------------------

df_players = eligible[
    eligible["Pos"].str.contains("DF", na=False)
]

df_threshold = (
    df_players["DefActionsPer90"]
    .quantile(0.85)
)

# ---------------------------------
# Goalkeepers
# ---------------------------------

gk = df[
    (df["Pos"].str.contains("GK", na=False))
    & (df["Age"] <= MAX_YOUNG_AGE)
    & (df["90s"] >= GK_MIN_90S)
]

gk_threshold = (
    gk["Save%"]
    .quantile(0.85)
)

print("\n===== THRESHOLDS =====")

print(
    f"FW GoalsPer90 85th percentile: "
    f"{fw_threshold:.3f}"
)

print(
    f"MF GoalContributionsPer90 85th percentile: "
    f"{mf_threshold:.3f}"
)

print(
    f"DF DefActionsPer90 85th percentile: "
    f"{df_threshold:.3f}"
)

print(
    f"GK Save% 85th percentile: "
    f"{gk_threshold:.3f}"
)
