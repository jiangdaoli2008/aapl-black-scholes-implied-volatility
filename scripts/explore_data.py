import pandas as pd


file = (
    "data/processed/"
    "AAPL_options_clean.csv"
)


df = pd.read_csv(file)


print("===================")
print("Basic information")
print("===================")

print(df.head())


print("\nShape:")
print(df.shape)



print("\nDate range:")

df["QUOTE_DATE"] = pd.to_datetime(
    df["QUOTE_DATE"]
)

print(
    df["QUOTE_DATE"].min()
)

print(
    df["QUOTE_DATE"].max()
)



print("\nUnderlying price statistics:")

print(
    df["UNDERLYING_LAST"]
    .describe()
)



# choose latest date

latest_date = (
    df["QUOTE_DATE"].max()
)


print("\nLatest date:")
print(latest_date)



latest = df[
    df["QUOTE_DATE"]
    ==
    latest_date
]


print(
    "\nOptions on latest date:"
)

print(
    latest.shape
)



print(
    "\nExpiration dates:"
)

print(
    latest["EXPIRE_DATE"]
    .unique()[:20]
)



print(
    "\nDTE distribution:"
)

print(
    latest["DTE"]
    .describe()
)