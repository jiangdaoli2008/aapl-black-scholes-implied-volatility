from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "results" / "AAPL_IV_comparison.csv"
OUTPUT_FILE = ROOT / "results" / "AAPL_volatility_smile.png"

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "MONEYNESS",
    "CALCULATED_IV",
    "C_IV",
    "QUOTE_DATE",
    "EXPIRE_DATE",
]
missing = set(required_columns) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

for column in ["MONEYNESS", "CALCULATED_IV", "C_IV"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

plot_df = (
    df.dropna(subset=["MONEYNESS", "CALCULATED_IV", "C_IV"])
    .sort_values("MONEYNESS")
)

if plot_df.empty:
    raise ValueError("No valid rows are available for plotting.")

if df["QUOTE_DATE"].nunique() != 1 or df["EXPIRE_DATE"].nunique() != 1:
    raise ValueError("The plot requires one quote date and one expiration date.")

quote_date = str(df["QUOTE_DATE"].iloc[0])[:10]
expire_date = str(df["EXPIRE_DATE"].iloc[0])[:10]

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    plot_df["MONEYNESS"],
    plot_df["CALCULATED_IV"],
    marker="o",
    label="Calculated IV",
)
ax.plot(
    plot_df["MONEYNESS"],
    plot_df["C_IV"],
    marker="s",
    linestyle="--",
    label="Provided IV",
)

ax.set(
    title=f"AAPL Call Implied Volatility\n{quote_date} | Expiry {expire_date}",
    xlabel="Moneyness (K/S)",
    ylabel="Implied volatility",
)
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
ax.grid(alpha=0.3)
ax.legend()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
fig.tight_layout()
fig.savefig(OUTPUT_FILE, dpi=150)
plt.close(fig)

print(f"Plotted samples: {len(plot_df)}")
print(f"Figure saved to: {OUTPUT_FILE}")