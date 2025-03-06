import pandas as pd
import os
from tabulate import tabulate
# Define the correct path
file_path = os.path.join("data", "blindern.csv")  # Replace with the actual CSV file name



# Read CSV with ';' as the separator
df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

data_dict = {row.iloc[2]: row.iloc[3:].tolist() for _, row in df.iterrows()}
try:
    data_list = [[key] + values for key, values in list(data_dict.items())[:100]]
except IndexError:
    print("Juster antall elementer")
header=["Dato","Maksimumtemperatur", "Minimumtemperatur", "Nedbør(døgn)", "Høyest middelvind", "Snødybde(cm)"]
# Print a sample
#print(list(data_dict.items())[:100])  # Print first 5 items

print(tabulate(data_list, headers=header,tablefmt="fancy_grid"))