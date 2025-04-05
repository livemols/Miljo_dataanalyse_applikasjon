import pandas as pd
import numpy as np
import sys 
import os 

#Find absolute path til data-file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Finds folder where this file is
data_path = os.path.join(current_dir, "..","..", "data")  # Go two folders up, then into data/

#Spesifi the filename
filename1 = "weather.csv"  
filename2 = "wind.csv"

#Make full path til the file
og_weather_file = os.path.join(data_path, filename1)
og_wind_file = os.path.join(data_path,filename2)

#Read raw data
weather_df = pd.read_csv(og_weather_file,skipfooter=1, engine='python',delimiter=";")
wind_df = pd.read_csv(og_wind_file,skipfooter=1, engine='python',delimiter=";")

#Drop weather station information for wind file
columns_to_drop=["Navn","Stasjon"]
wind_df.drop(columns=columns_to_drop, inplace=True)

#Merges the files on the same dates
merged_df=pd.merge(weather_df,wind_df,on="Tid(norsk normaltid)")

#Make a new file and put in into the data folder
merged_file_path=os.path.join(data_path,"merged.csv")
merged_df.to_csv(merged_file_path,index=False)



print("suksess")


