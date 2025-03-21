import pandas as pd
import os
import sys
from tabulate import tabulate
from datetime import datetime





# Manuelt setter file-path til blindern.csv
file_path = r"C:\Users\Tai khoan chung\OneDrive - NTNU\Anvendt prog\Mappe innlevering\Miljo_dataanalyse_applikasjon\data\blindern.csv"


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







