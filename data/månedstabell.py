# from testnat.py
import pandas as pd
import os
from tabulate import tabulate

# Define the correct path
file_path = os.path.join("data", "blindern.csv")  # Replace with the actual CSV file name

df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")

data_dict = {row.iloc[2]: row.iloc[3:].tolist() for _, row in df.iterrows()}
try:
    data_list = [[key] + values for key, values in list(data_dict.items())[:100]]
except IndexError:
    print("Juster antall elementer")
header=["Dato","Maksimumtemperatur", "Minimumtemperatur", "Nedbør(døgn)", "Høyest middelvind", "Snødybde(cm)"]
# Print a sample
#print(list(data_list))  # Print first 100 items

#print(tabulate(data_list, headers=header,tablefmt="fancy_grid"))
#from testnat.py ^^^^



#Get the average values for the different months in the data set.
def average_monthly():
    i=0
    monthly_average=[]

    while i < len(data_list):
        days_in_month=0
        max_temp, min_temp, rain, wind, snow= 0,0,0,0,0
        current_date=data_list[i][0]
        current_day, current_month, current_year=current_date.split(".")

        while i < len(data_list):
            next_date=data_list[i][0]
            next_day, next_month, next_year=next_date.split(".")
            


            if current_month==next_month and current_year==next_year:
                max_temp+=int(data_list[i][1])
                min_temp+=int(data_list[i][2])
                rain+=int(data_list[i][3])
                wind+=int(data_list[i][4])
                snow+=int(data_list[i][5])
                days_in_month+=1
                i+=1

            else:
                break
          
        avg_max_temp=max_temp/days_in_month
        avg_min_temp=min_temp/days_in_month
        avg_rain=rain/days_in_month
        avg_wind=wind/days_in_month
        avg_snow=snow/days_in_month

        li=[current_month,avg_max_temp,avg_min_temp,avg_rain,avg_wind,avg_snow]
        monthly_average.append(li)
        
    print (tabulate(monthly_average,headers=header,tablefmt="fancy_grid"))

average_monthly()

        





