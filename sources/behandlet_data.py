#Denne filen renser og behandler dataen vår

import pandas as pd
import os
import numpy as np

# Finn absolutt sti til data-mappen
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finner mappen der testnat.py er
data_path = os.path.join(current_dir, "..", "data")  # Går én mappe opp, deretter inn i data/

# Spesifiser filnavnet
filename = "blindern.csv"  

# Lag full sti til filen
original_file = os.path.join(data_path, filename)
modified_file = os.path.join(data_path, "blindern_behandlet.csv")  

# Read the original CSV file
df = pd.read_csv(original_file, delimiter=";")

# Apply modifications
df.columns = ["Navn", "Stasjon", "Tid", "Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]
df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")

# Convert columns to numeric
df[["Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]] = df[["Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]].apply(pd.to_numeric, errors='coerce')

#Delete duplitcates (rows)
df.drop_duplicates(inplace = True)

# Outlier removal

threshold = 3

for column in df.select_dtypes(include=['number']).columns:
    mean = df[column].mean()
    std = df[column].std()
    lower_limit = mean - threshold * std
    upper_limit = mean + threshold * std

    # ".where" for å beholde NaN i stedet for å fjerne verdier helt
    df[column] = df[column].where(df[column].between(lower_limit, upper_limit))


# Time series data processing + missing data

for column in df.select_dtypes(include=['number']).columns:
    if column in ["Makstemp", "Mintemp"]:
        df[column] = df[column].interpolate(method='polynomial', order=2).round(1)
    if column in ["Nedbør", "Vind", "Snø"]:
        df[column] = df[column].interpolate(method='linear').round(1)
        df[column] = df[column].clip(lower = 0)
        


# Save the modified DataFrame as a new CSV file in the same folder
df.to_csv(modified_file, index=False, sep=";")  # Keep the same delimiter (;)

print(f"Modified CSV file saved as: {modified_file}")

