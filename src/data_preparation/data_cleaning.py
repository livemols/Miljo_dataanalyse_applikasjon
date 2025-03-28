#Denne filen renser og behandler dataen vår
import pandas as pd
import os
import numpy as np
import numpy.ma as ma

# Finn absolutt sti til data-mappen
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finner mappen der testnat.py er
data_path = os.path.join(current_dir, "..","..", "data")  # Går én mappe opp, deretter inn i data/

# Spesifiser filnavnet
filename = "blindern_skitten.csv"  

# Lag full sti til filen
original_file = os.path.join(data_path, filename)
modified_file = os.path.join(data_path, "blindern_behandlet.csv")  

# leser rådata
df = pd.read_csv(original_file,skipfooter=1, engine='python',delimiter=";")

# Endrer navn på kolonnene for bedre oversikt og gjorde om dato til datetime format
df.columns = ["Navn", "Stasjon", "Tid", "Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]
df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")




#Behandler manglende data ved interpolate
#Endrer alle mising value "-" til Nan og deretter bruker interpolate
df = df.replace("-", np.nan) 

df.interpolate(method='linear', inplace=True)
df=df.round(1)

# lagrer DataFrame til ny cvs fil i samme mappe
df.to_csv(modified_file, index=False, sep=";")  # Holder den samme delimiter (;)






print(f"Modified CSV file saved as: {modified_file}")

