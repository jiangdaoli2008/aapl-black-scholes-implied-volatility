import pandas as pd
import os


# ==========================
# File paths
# ==========================

input_file = (
    "data/raw/AAPL_options.csv"
)

output_file = (
    "data/processed/"
    "AAPL_options_clean.csv"
)


os.makedirs(
    "data/processed",
    exist_ok=True
)


# ==========================
# Columns we need
# ==========================

use_columns = [
    "QUOTE_DATE",
    "UNDERLYING_LAST",
    "EXPIRE_DATE",
    "DTE",
    "STRIKE",
    "C_BID",
    "C_ASK",
    "C_LAST",
    "C_IV"
]


# ==========================
# Read data by chunks
# ==========================

chunks = []

print("Reading data...")


# ==========================
# Read CSV header first
# ==========================

raw_columns = pd.read_csv(
    input_file,
    nrows=0
).columns


clean_columns = (
    raw_columns
    .str.strip()
    .str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
)


column_mapping = dict(
    zip(
        raw_columns,
        clean_columns
    )
)


print("Available columns after cleaning:")
print(clean_columns.tolist())


# columns we need after cleaning

required_columns = [
    "QUOTE_DATE",
    "UNDERLYING_LAST",
    "EXPIRE_DATE",
    "DTE",
    "STRIKE",
    "C_BID",
    "C_ASK",
    "C_LAST",
    "C_IV"
]


# find original names

selected_original_columns = [
    key
    for key, value in column_mapping.items()
    if value in required_columns
]


print("\nSelected raw columns:")
print(selected_original_columns)



for chunk in pd.read_csv(
        input_file,
        usecols=selected_original_columns,
        chunksize=100000
):

    chunk.columns = (
        chunk.columns
        .str.strip()
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
    )

    chunks.append(chunk)

    # clean column names

    chunk.columns = (
        chunk.columns
        .str.strip()
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
    )


    chunks.append(chunk)


df = pd.concat(
    chunks,
    ignore_index=True
)


print(
    "Original shape:",
    df.shape
)


# ==========================
# Date conversion
# ==========================

df["QUOTE_DATE"] = pd.to_datetime(
    df["QUOTE_DATE"]
)


df["EXPIRE_DATE"] = pd.to_datetime(
    df["EXPIRE_DATE"]
)


# ==========================
# Numeric conversion
# ==========================

numeric_columns = [
    "UNDERLYING_LAST",
    "DTE",
    "STRIKE",
    "C_BID",
    "C_ASK",
    "C_LAST",
    "C_IV"
]


for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# ==========================
# Create market price
# ==========================

print(
    "Creating option market price..."
)


# midpoint

df["MARKET_PRICE"] = (
    df["C_BID"]
    +
    df["C_ASK"]
) / 2


# if bid/ask invalid use last price

invalid_mid = (
    df["C_BID"].isna()
    |
    df["C_ASK"].isna()
    |
    (df["C_BID"] <= 0)
    |
    (df["C_ASK"] <= 0)
)


df.loc[
    invalid_mid,
    "MARKET_PRICE"
] = df.loc[
    invalid_mid,
    "C_LAST"
]


# ==========================
# Remove invalid observations
# ==========================

df = df.dropna(
    subset=[
        "UNDERLYING_LAST",
        "STRIKE",
        "DTE",
        "MARKET_PRICE"
    ]
)


# option price must be positive

df = df[
    df["MARKET_PRICE"] > 0
]


# maturity

df = df[
    df["DTE"] > 0
]


# ==========================
# Save
# ==========================


final_columns = [
    "QUOTE_DATE",
    "UNDERLYING_LAST",
    "EXPIRE_DATE",
    "DTE",
    "STRIKE",
    "MARKET_PRICE",
    "C_IV",
    "C_BID",
    "C_ASK"
]


df = df[
    final_columns
]


print(
    "Final shape:",
    df.shape
)


df.to_csv(
    output_file,
    index=False
)


print(
    "Saved:"
)

print(output_file)