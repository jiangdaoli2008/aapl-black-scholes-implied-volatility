import pandas as pd


file = (
    "data/processed/"
    "AAPL_research_sample.csv"
)


df = pd.read_csv(file)


print("===================")
print("Research sample")
print("===================")


print(df)


print("\nSpot price:")

print(
    df["UNDERLYING_LAST"].iloc[0]
)


print("\nStrike range:")

print(
    df["STRIKE"].min()
)

print(
    df["STRIKE"].max()
)


print("\nMarket price range:")

print(
    df["MARKET_PRICE"].min()
)

print(
    df["MARKET_PRICE"].max()
)


print("\nProvided IV range:")

print(
    df["C_IV"].min()
)

print(
    df["C_IV"].max()
)