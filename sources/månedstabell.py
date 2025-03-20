# from testnat.py
import pandas as pd
import os
from tabulate import tabulate

# Define the correct path
file_path = os.path.join("data", "blindern.csv")  # Replace with the actual CSV file name

df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

data_dict = {row.iloc[2]: row.iloc[3:].tolist() for _, row in df.iterrows()}
try:
    data_list = [[key] + values for key, values in list(data_dict.items())[:3000]]
except IndexError:
    print("Juster antall elementer")
header=["Dato","år","Maksimumtemperatur", "Minimumtemperatur", "Nedbør(døgn)", "Høyest middelvind", "Snødybde(cm)"]
# Print a sample
#print(list(data_list))  # Print first 100 items

#print(tabulate(data_list, headers=header,tablefmt="fancy_grid"))
#from testnat.py ^^^^

def månde():
    maxtemp,mintemp,rain,wind,snow=0,0,0,0,0
    dager=0
    tab=[]
    for i in range(len(data_list)-1):
        month1 = data_list[i][0].split('.')[1]  
        year = data_list[i][0].split('.')[2]
        month2 = data_list[i + 1][0].split('.')[1]  
        if month1==month2:
            try:
                maxtemp+=int(data_list[i][1])
                mintemp+=int(data_list[i][2])
                rain+=int(data_list[i][3])
                wind+=int(data_list[i][4])
                snow+=int(data_list[i][5])
                dager+=1
            except ValueError:
                pass
        else:
            if 0<dager:
                avrmax=maxtemp/dager
                avrmin=mintemp/dager
                avg_rain=rain/dager
                avg_wind=wind/dager
                avg_snow=snow/dager
                li=[month1,year,avrmax,avrmin,avg_rain,avg_wind,avg_snow]
                tab.append(li)
                dager,maxtemp,mintemp,rain,wind,snow=0,0,0,0,0,0
    print(tabulate(tab, headers=header,tablefmt="fancy_grid"))

månde()
