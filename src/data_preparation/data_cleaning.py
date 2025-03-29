#Denne filen lager klassen data_cleaning som brukes til å rense data

import pandas as pd
import numpy as np

class data_cleaning:
    def form(df):
        # Change the headers of the columm for better overview, and change the date to datetime format
        df.columns = ["Navn", "Stasjon", "Tid", "Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]
        df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")

        # Convert columns to numeric
        df[["Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]] = df[["Makstemp", "Mintemp", "Nedbør", "Vind", "Snø"]].apply(pd.to_numeric, errors='coerce')
    
    def duplicates(df):
        #Delete duplitcates (rows)
        df.drop_duplicates(inplace = True)
    
    def missing(df):
        #convert all "-" to Nan
        df = df.replace("-", np.nan) 
        
    
    def outliers(df):
        threshold = 3

        for column in df.select_dtypes(include=['number']).columns:
            mean = df[column].mean()
            std = df[column].std()
            lower_limit = mean - threshold * std
            upper_limit = mean + threshold * std

            # ".where" for å beholde NaN i stedet for å fjerne verdier helt
            df[column] = df[column].where(df[column].between(lower_limit, upper_limit))

    def replacing(df):
        # Time series data processing + missing data

        for column in df.select_dtypes(include=['number']).columns:
            if column in ["Makstemp", "Mintemp"]:
                df[column] = df[column].interpolate(method='polynomial', order=2).round(1)
            if column in ["Nedbør", "Vind", "Snø"]:
                df[column] = df[column].interpolate(method='linear').round(1)
                df[column] = df[column].clip(lower = 0)














