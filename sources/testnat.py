import pandas as pd
import os
import sys
from tabulate import tabulate
from datetime import datetime


# Finn absolutt sti til data-mappen
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finner mappen der testnat.py er
data_path = os.path.join(current_dir, "..", "data")  # Går én mappe opp, deretter inn i data/

# Spesifiser filnavnet
filename = "blindern.csv"  

# Lag full sti til filen
file_path = os.path.join(data_path, filename)


# sorterer data etter ";"
df = pd.read_csv(file_path,delimiter=";")


script_dir = os.path.dirname(os.path.abspath(__file__))


os.chdir(script_dir)


#behandler blindern.cvs
df.columns=["Navn", "Stasjon", "Tid","Makstemp", "Mintemp", "Nedbør", "Vind","Snø"]
df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")
df.reset_index()
# Adderer en ny kolonne for månde
df['Month'] = df['Tid'].dt.month
#Siden "Snø"-kolonne inneholder noen ikke-målte verdier "-", blir disse verdiene bytte om til Nan for å unngå påvirking til gjennomsnitt beregningen
df['Snø'] = pd.to_numeric(df['Snø'], errors='coerce') 

# Sorterer etter månde og regne ut gjennomsnitt for alle kolonne
monthly_means = df.groupby('Month').mean(numeric_only=True)

print(monthly_means)







