import pandas as pd
import os
import sys
from tabulate import tabulate
from datetime import datetime



# Finn absolutt sti til data-mappen
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finner mappen der testnat.py er
data_path = os.path.join(current_dir, "..", "data")  # Går én mappe opp, deretter inn i data/

# Spesifiser filnavnet
filename = "blindern_behandlet.csv"  

# Lag full sti til filen
file_path = os.path.join(data_path, filename)


# sorterer data etter ";" og gjør om "Tid" kolonne til datetime format
df = pd.read_csv(file_path,delimiter=";",parse_dates=['Tid'])


script_dir = os.path.dirname(os.path.abspath(__file__))


os.chdir(script_dir)

print(df)



# Adderer en ny kolonne for månde
df['Month'] = df['Tid'].dt.month

# Sorterer etter månde og regne ut gjennomsnitt for alle kolonne
monthly_means = df.groupby('Month').mean(numeric_only=True)



print(tabulate(monthly_means, tablefmt="fancy_grid",headers=["Månde", "Maxtemp", "Mintemp", "Nedbør","Vind", "Snø", ]))
print(monthly_means.plot(kind="bar", title="Gjennomsnittlig målinger"))