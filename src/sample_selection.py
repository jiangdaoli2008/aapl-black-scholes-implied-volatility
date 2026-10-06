import pandas as pd


input_file = (
    "data/processed/"
    "AAPL_options_clean.csv"
)


output_file = (
    "data/processed/"
    "AAPL_research_sample.csv"
)



df = pd.read_csv(
    input_file
)


df["QUOTE_DATE"] = pd.to_datetime(
    df["QUOTE_DATE"]
)


df["EXPIRE_DATE"] = pd.to_datetime(
    df["EXPIRE_DATE"]
)



# =====================
# Research setting
# =====================

quote_date = pd.Timestamp(
    "2020-12-31"
)


expiration = pd.Timestamp(
    "2021-02-19"
)



sample = df[
    (df["QUOTE_DATE"] == quote_date)
    &
    (df["EXPIRE_DATE"] == expiration)
]


print(
    "After date and expiration selection:"
)

print(sample.shape)



# =====================
# Remove invalid data
# =====================

sample = sample[
    sample["MARKET_PRICE"] > 0
]


sample = sample[
    sample["STRIKE"] > 0
]



# =====================
# Moneyness filter
# =====================

spot = sample[
    "UNDERLYING_LAST"
].iloc[0]


sample["MONEYNESS"] = (
    sample["STRIKE"]
    /
    spot
)


sample = sample[
    (sample["MONEYNESS"] >= 0.8)
    &
    (sample["MONEYNESS"] <= 1.2)
]


sample = sample.drop_duplicates(
    subset=[
        "QUOTE_DATE",
        "EXPIRE_DATE",
        "STRIKE"
    ]
)
# =====================
# Sort
# =====================

sample = sample.sort_values(
    "STRIKE"
)



print(
    "Final sample:"
)

print(sample.shape)



sample.to_csv(
    output_file,
    index=False
)


print(
    "Saved:"
)

print(output_file)