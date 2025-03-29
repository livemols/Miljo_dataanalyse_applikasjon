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

#Delete duplitcates (rows)
df.drop_duplicates(inplace = True)

# Outlier removal

threshold = 3
modified_file = df.copy()

for column in df.columns:
    mean = df[column].mean()
    std = df[column].std()
    lower_limit = mean - threshold * std
    upper_limit = mean + threshold * std

    # ".where" for å beholde NaN i stedet for å fjerne verdier helt
    modified_file[column] = df[column].where(df[column].between(lower_limit, upper_limit))

# Time series data processing

for column in modified_file.columns:
    modified_file[column] = modified_file[column].interpolate(method='polynomial', order=2)



# Save the modified DataFrame as a new CSV file in the same folder
df.to_csv(modified_file, index=False, sep=";")  # Keep the same delimiter (;)

print(f"Modified CSV file saved as: {modified_file}")

