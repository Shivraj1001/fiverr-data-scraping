import pandas as pd

df = pd.read_csv("adv5.csv")
df = df.drop_duplicates().dropna()
df.to_excel("adv6_cleaned.xlsx", index=False)

