import sys
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import PROCESSED_FILE

df = pd.read_csv(PROCESSED_FILE, encoding="utf-8")

print(df.columns.tolist())
