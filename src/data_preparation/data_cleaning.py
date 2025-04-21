# This file make the class data_cleaning for cleaning data

import pandas as pd
import numpy as np

class DataCleaning:

    def __init__(self, df):
        self.df = df

    def form(self):
        # Change the headers of the columm for better overview, and change the date to datetime format
        self.df.columns = ["Navn", "Stasjon", "Tid", "Makstemp", "Mintemp", "Middeltemp","Snø","Nedbør","Middelvind" ,"Høye vindkast"]
        self.df["Tid"] = pd.to_datetime(self.df["Tid"], format="%d.%m.%Y")

        # Convert columns to numeric
        numeric_columns = ["Makstemp", "Mintemp","Middeltemp", "Snø", "Nedbør", "Middelvind", "Høye vindkast"]
        self.df[numeric_columns] = self.df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
        return self
    
    def duplicates(self):
        # Delete duplitcates (rows)
        self.df.drop_duplicates(inplace = True)

        return self

    
    def missing(self):
        # Convert all "-" to Nan
        self.df = self.df.replace("-", np.nan) 
        
        return self

    def outliers(self):

        threshold = 3.5

        for column in self.df.select_dtypes(include=['number']).columns:
            
            if column in ["Snø","Nedbør"]:
                threshold = 10

            self.df[column] = self.df[column].where(self.df[column].between(-40, 200))
            
            mean = self.df[column].mean()
            std = self.df[column].std()
            lower_limit = mean - threshold * std
            upper_limit = mean + threshold * std

             # Change outliers to NaN
            self.df[column] = self.df[column].where(self.df[column].between(lower_limit, upper_limit))

        return self

    def replacing(self):
        # Time series data processing + missing data
        
        for column in self.df.select_dtypes(include=['number']).columns:
            self.df[column] = self.df[column].interpolate(method='linear').round(1)
            if column in ["Snø", "Nedbør", "Middelvind","Høye vindkast"]:
                self.df[column] = self.df[column].clip(lower = 0)
        
        return self
    

















