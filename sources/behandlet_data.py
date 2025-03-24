#Denne filen renser og behandler dataen vår
import pandas as pd
import os

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

# Save the modified DataFrame as a new CSV file in the same folder
df.to_csv(modified_file, index=False, sep=";")  # Keep the same delimiter (;)

print(f"Modified CSV file saved as: {modified_file}")

