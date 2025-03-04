import pandas as pd
import os

# Define the correct path
file_path = os.path.join("data", "blindern.csv")  # Replace with the actual CSV file name



# Read CSV with ';' as the separator
df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

data_dict = {row.iloc[2]: row.iloc[3:].tolist() for _, row in df.iterrows()}

# Print a sample
print(list(data_dict.items())[:100])  # Print first 5 items

