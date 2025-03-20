import pandas as pd
import os
from tabulate import tabulate
from datetime import datetime



# Define the correct path
file_path = os.path.join("data", "blindern.csv")  

script_dir = os.path.dirname(os.path.abspath(__file__))


os.chdir(script_dir)


df=pd.read_csv("blindern.csv",delimiter=";")
df.columns=["Navn", "Stasjon", "Tid","Makstemp", "Mintemp", "Nedbør", "Vind","Snø"]
df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")
df.reset_index()


gjennomsnitt=[]
for i in range(1,13):
    maxtemp,mintemp,rain,wind,snow=0,0,0,0,0
    
    dager=0
    for k in range(len(df)):
        if df["Tid"][k].month==i:
            try:
                maxtemp+=df["Makstemp"][k]
                mintemp+=df["Mintemp"][k]
                rain+=df["Nedbør"][k]
                wind+=df["Vind"][k]
                snow+=float(df["Snø"][k])


                dager+=1
                month=df["Tid"][k].month
            except ValueError:
                maxtemp+=df["Makstemp"][k]
                mintemp+=df["Mintemp"][k]
                rain+=df["Nedbør"][k]
                wind+=df["Vind"][k]
                


                dager+=1
                
    if 0<dager:   
        avr_maxtemp=float(maxtemp/dager)
        avr_mintemp=float(mintemp/dager)
        avr_rain=float(rain/dager)
        avr_wind=float(wind/dager)
        avr_snow=float(snow/dager)
    else:
        # If dager is 0, set averages to a default value (e.g., 0 or None)
        avr_maxtemp = avr_mintemp = avr_rain = avr_wind = avr_snow = 0
        
    
    mande = [month,round(avr_maxtemp, 2), round(avr_mintemp, 2), round(avr_rain, 2), round(avr_wind, 2), round(avr_snow, 2)]
    gjennomsnitt.append(mande)

header=["Måned","Maksimumtemperatur", "Minimumtemperatur", "Nedbør(døgn)", "Høyest middelvind", "Snødybde(cm)"]
            
print(tabulate(gjennomsnitt, headers=header,tablefmt="fancy_grid"))

#print(df)


