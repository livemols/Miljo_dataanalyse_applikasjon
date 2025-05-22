# This file make the class data_cleaning for cleaning data

import pandas as pd
import numpy as np

class DataCleaning:

    def __init__(self, df):
        self.df = df

    def form(self):
        # Change the headers of the columm for better overview, and change the date to datetime format
        try:
            self.df.columns = ["Navn", "Stasjon", "Tid", "Makstemp", "Mintemp", "Middeltemp","Snø","Nedbør","Middelvind" ,"Høye vindkast"]
            self.df["Tid"] = pd.to_datetime(self.df["Tid"], format="%d.%m.%Y")

            # Convert columns to numeric
            numeric_columns = ["Makstemp", "Mintemp","Middeltemp", "Snø", "Nedbør", "Middelvind", "Høye vindkast"]
            self.df[numeric_columns] = self.df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
            return self
        except AttributeError:
            print("Unexpected input: The input must be a Dataframe.")
        except ValueError:
            print("Value Error: could be number conversion")
        except TypeError:
            print("Type Error: could be conversion of incompatible type")
    
    def duplicates(self):
        try:
            # Delete duplitcates (rows)
            self.df.drop_duplicates(inplace = True)

            return self
        except AttributeError:
            print("Unexpected input: The input must be a Dataframe.")
        except TypeError:
            print("Type Error: passing of invalid arguments.")

    
    def missing(self):
        try:
            # Convert all "-" to Nan
            self.df = self.df.replace("-", np.nan) 
            
            return self
        except TypeError as te:
            print(f"TypeError: {te}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def outliers(self):
        try:
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
        except TypeError as te:
            print(f"TypeError: {te}")
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def replacing(self):
        # Time series data processing + missing data
        try:
            for column in self.df.select_dtypes(include=['number']).columns:
                self.df[column] = self.df[column].interpolate(method='linear').round(1)
                if column in ["Snø", "Nedbør", "Middelvind","Høye vindkast"]:
                    self.df[column] = self.df[column].clip(lower = 0)
            
            return self
        except TypeError as te:
            print(f"TypeError: {te}")
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    
    

















