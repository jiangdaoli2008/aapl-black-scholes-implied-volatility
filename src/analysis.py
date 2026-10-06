from pathlib import Path

import numpy as np
import pandas as pd

from src.implied_vol import implied_volatility


# =====================================
# Project paths
# =====================================

ROOT = Path(__file__).resolve().parents[1]


input_file = (
    ROOT
    /
    "data"
    /
    "processed"
    /
    "AAPL_research_sample.csv"
)


output_file = (
    ROOT
    /
    "results"
    /
    "AAPL_IV_comparison.csv"
)



# =====================================
# Model assumptions
# =====================================

risk_free_rate = 0.001

dividend_yield = 0.0



# =====================================
# Load data
# =====================================

print("Loading research sample...")


df = pd.read_csv(input_file)


if df.empty:
    raise ValueError(
        "Research sample is empty."
    )


print("\nOriginal shape:")
print(df.shape)



# =====================================
# Required columns
# =====================================

required_columns = [
    "QUOTE_DATE",
    "EXPIRE_DATE",
    "UNDERLYING_LAST",
    "STRIKE",
    "DTE",
    "MARKET_PRICE",
    "C_IV",
]


missing = (
    set(required_columns)
    -
    set(df.columns)
)


if missing:
    raise ValueError(
        f"Missing columns: {sorted(missing)}"
    )



# =====================================
# Data type conversion
# =====================================


numeric_columns = [
    "UNDERLYING_LAST",
    "STRIKE",
    "DTE",
    "MARKET_PRICE",
    "C_IV",
]


for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )



# =====================================
# Date processing
# =====================================


df["QUOTE_DATE"] = pd.to_datetime(
    df["QUOTE_DATE"],
    errors="coerce"
)


df["EXPIRE_DATE"] = pd.to_datetime(
    df["EXPIRE_DATE"],
    errors="coerce"
)



if (
    df[["QUOTE_DATE", "EXPIRE_DATE"]]
    .isna()
    .any()
    .any()
):

    raise ValueError(
        "Invalid or missing dates."
    )



if (
    df["EXPIRE_DATE"]
    <=
    df["QUOTE_DATE"]
).any():

    raise ValueError(
        "Expiration date must be after quote date."
    )



# =====================================
# Research sample validation
# =====================================


print("\nQuote dates:")
print(df["QUOTE_DATE"].unique())


print("\nExpiration dates:")
print(df["EXPIRE_DATE"].unique())


if df["QUOTE_DATE"].nunique() != 1:

    raise ValueError(
        "Sample must contain one quote date only."
    )


if df["EXPIRE_DATE"].nunique() != 1:

    raise ValueError(
        "Sample must contain one expiration date only."
    )



# =====================================
# Check DTE consistency
# =====================================


calculated_dte = (
    df["EXPIRE_DATE"]
    -
    df["QUOTE_DATE"]
).dt.days


dte_difference = (
    calculated_dte
    -
    df["DTE"]
).abs()



if dte_difference.max() > 1:

    print(
        "\nWarning:"
        " DTE differs from calendar date difference."
    )



# =====================================
# Calculate moneyness
# =====================================


df["MONEYNESS"] = (
    df["STRIKE"]
    /
    df["UNDERLYING_LAST"]
)



# =====================================
# Check C_IV scale
# =====================================


print("\nProvided market IV statistics:")

print(
    df["C_IV"].describe()
)


max_iv = df["C_IV"].max()


if max_iv > 5:

    print(
        "\nConverting C_IV from percentage to decimal."
    )

    df["C_IV"] = (
        df["C_IV"]
        /
        100
    )



# =====================================
# Calculate implied volatility
# =====================================


def calculate_iv(row):

    values = row[
        [
            "UNDERLYING_LAST",
            "STRIKE",
            "DTE",
            "MARKET_PRICE",
        ]
    ]


    if not np.isfinite(
        values.to_numpy(dtype=float)
    ).all():

        return np.nan



    return implied_volatility(
        market_price=row["MARKET_PRICE"],
        S=row["UNDERLYING_LAST"],
        K=row["STRIKE"],
        T=row["DTE"] / 365,
        r=risk_free_rate,
        q=dividend_yield,
    )



print(
    "\nCalculating implied volatility..."
)


df["CALCULATED_IV"] = df.apply(
    calculate_iv,
    axis=1
)



# =====================================
# Compare IV
# =====================================


df["IV_DIFFERENCE"] = (
    df["CALCULATED_IV"]
    -
    df["C_IV"]
)



# =====================================
# Save results
# =====================================


output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_csv(
    output_file,
    index=False
)



# =====================================
# Summary
# =====================================


print("\n====================")
print("Analysis Summary")
print("====================")


print(
    f"Total samples: {len(df)}"
)


print(
    "Successful IV calculations:",
    df["CALCULATED_IV"].notna().sum()
)


print(
    "Failed IV calculations:",
    df["CALCULATED_IV"].isna().sum()
)



print("\nResult preview:")


print(
    df[
        [
            "STRIKE",
            "MONEYNESS",
            "MARKET_PRICE",
            "CALCULATED_IV",
            "C_IV",
            "IV_DIFFERENCE",
        ]
    ]
)



print("\nSaved result:")

print(output_file)