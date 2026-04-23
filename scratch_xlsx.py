import pandas as pd

df = pd.read_excel("holdings/_temp_download.xlsx", header=None)
print("First 20 rows:")
for i in range(min(20, len(df))):
    print(f"Row {i}: {list(df.iloc[i])}")
