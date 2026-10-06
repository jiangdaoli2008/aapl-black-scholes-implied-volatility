from pathlib import Path

import numpy as np
import pandas as pd

from src.bs_model import black_scholes_call


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "results" / "AAPL_IV_comparison.csv"
OUTPUT_FILE = ROOT / "results" / "AAPL_IV_validation.csv"

# Use the same assumptions as analysis.py.
RISK_FREE_RATE = 0.001
DIVIDEND_YIELD = 0.0

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "UNDERLYING_LAST",
    "STRIKE",
    "DTE",
    "MARKET_PRICE",
    "CALCULATED_IV",
]

missing = set(required_columns) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

for column in required_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

valid = (
    np.isfinite(df[required_columns].to_numpy(dtype=float)).all(axis=1)
    & (df["UNDERLYING_LAST"] > 0)
    & (df["STRIKE"] > 0)
    & (df["DTE"] > 0)
    & (df["MARKET_PRICE"] >= 0)
    & (df["CALCULATED_IV"] >= 0)
)

df["REPRICED_CALL"] = np.nan

# Reprice each valid option using its calculated implied volatility.
for index, row in df.loc[valid].iterrows():
    df.loc[index, "REPRICED_CALL"] = black_scholes_call(
        S=row["UNDERLYING_LAST"],
        K=row["STRIKE"],
        T=row["DTE"] / 365,
        r=RISK_FREE_RATE,
        sigma=row["CALCULATED_IV"],
        q=DIVIDEND_YIELD,
    )

df["PRICING_ERROR"] = df["REPRICED_CALL"] - df["MARKET_PRICE"]
df["ABS_PRICING_ERROR"] = df["PRICING_ERROR"].abs()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Total samples: {len(df)}")
print(f"Validated samples: {valid.sum()}")
print(f"Skipped samples: {(~valid).sum()}")

if valid.any():
    print(
        "Maximum absolute pricing error:",
        f"{df['ABS_PRICING_ERROR'].max():.10f}",
    )
    print(
        "Mean absolute pricing error:",
        f"{df['ABS_PRICING_ERROR'].mean():.10f}",
    )

print(f"Validation results saved to: {OUTPUT_FILE}")