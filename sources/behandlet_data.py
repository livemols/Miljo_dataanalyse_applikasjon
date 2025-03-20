#Denne filen renser og behandler dataen vår
import pandas as pd
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file paths for original and modified CSV
original_file = os.path.join(script_dir, "blindern.csv")  
modified_file = os.path.join(script_dir, "blindern_behandlet.csv")  

# Read the original CSV file
df = pd.read_csv(original_file, delimiter=";")

# Apply modifications
df.columns = ["Navn", "Stasjon", "Tid", "Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]
df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")

# Save the modified DataFrame as a new CSV file in the same folder
df.to_csv(modified_file, index=False, sep=";")  # Keep the same delimiter (;)

print(f"Modified CSV file saved as: {modified_file}")

