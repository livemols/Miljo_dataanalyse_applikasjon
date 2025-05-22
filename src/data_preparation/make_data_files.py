import pandas as pd
import numpy as np
import sys
import os


class MakeDataFiles:
    def combine_files(self,filename1 = "weather.csv",filename2 = "wind.csv"):

        current_dir = os.path.dirname(os.path.abspath(__file__))  # Finds folder where this file is
        data_path = os.path.join(current_dir, "..","..", "data")  # Go two folders up, then into data/

        # Make full path til the file
        og_weather_file = os.path.join(data_path, filename1)
        og_wind_file = os.path.join(data_path,filename2)

        # Read raw data
        weather_df = pd.read_csv(og_weather_file,skipfooter=1, engine='python',delimiter=";")
        wind_df = pd.read_csv(og_wind_file,skipfooter=1, engine='python',delimiter=";")

        # Drop weather station information for wind file
        columns_to_drop=["Navn","Stasjon"]
        wind_df.drop(columns=columns_to_drop, inplace=True)

        # Merges the files on the same dates
        merged_df=pd.merge(weather_df,wind_df,on="Tid(norsk normaltid)")

        # Make a new file and put in into the data folder
        merged_file_path=os.path.join(data_path,"blindern.csv")
        merged_df.to_csv(merged_file_path,index=False,sep=";")

        print("Filene er slått sammen")
        
    def make_dirty_data(self, filename = "blindern.csv", dirty_file = "blindern_dirty_data_generator.csv"):
        # Find absolute path to data-file
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Finds folder where this file is
        data_path = os.path.join(current_dir, "..","..", "data")  # Go two folders up, then into data/

        # Make full path til the file
        original_file = os.path.join(data_path, filename)
        modified_file = os.path.join(data_path, dirty_file)  

        # Read raw data
        df = pd.read_csv(original_file,skipfooter=1, engine='python',delimiter=";")

        # Add more missing value "-", because there were already "-" in the file.
        # Want 30% of the rows to change 
        frac = 0.3

        # Choose a random row and column and change the number to "-" 
        idx = np.random.choice(range(df.shape[0]), int(df.shape[0]*frac), replace=True)
        cols = np.random.choice([3,4,5,6,7], size=len(idx), replace=True)
        x = df.to_numpy()                                                   # My own concept and solution; ChatGPT was used to help translate it into code. 
        x[idx, cols] = "-"
        df=pd.DataFrame(x, index=df.index, columns=df.columns)

        # ADD DUPLICATES 
        # Choose the first 49 rows and add them to the end of DataFrame

        rows_to_duplicate=list(range(1,50))
        duplicates = df.iloc[rows_to_duplicate]  
        df = pd.concat([df, duplicates], ignore_index=True)   #ChatGpt assisted with buildt-in pandas functions

        # ADD OUTLIERS
        # Make a list with outliers
        outliers = np.array([200.5, 220.3, -500,-301, 400.5, 420.3, -200,-201])

        # Choose a random row and column and change the number to one from outliers
        idx1 = np.random.choice(range(df.shape[0]), int(df.shape[0]*frac), replace=True)
        cols1 = np.random.choice([3,4,5,6,7], size=len(idx1), replace=True)
        x1 = df.to_numpy()
        x1[idx1, cols1] = np.random.choice(outliers,size=len(idx1))
        df=pd.DataFrame(x1, index=df.index, columns=df.columns)

        # Make DataFrame to new csv file in the same folder
        df.to_csv(modified_file, index=False, sep=";")  # Keep the same delimiter (;)

        print(f"Modified CSV file saved as: {modified_file}")

    def clean_file(self,original_file = "blindern.csv",cleaned_file = "blindern_data_cleaning.csv"):
        sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '../src')))

        from data_preparation.data_cleaning import DataCleaning

        data_path = os.path.join(os.getcwd(),"..", "data")
        original_path = os.path.join(data_path, original_file)  
        df = pd.read_csv(original_path, delimiter=";")
        data_cleaner = DataCleaning(df)

        modified_file_original = os.path.join(data_path, cleaned_file)

        # Cleaning original file
        df = data_cleaner.form().duplicates().missing().outliers().replacing().df

        # Save the modified DataFrame as a new CSV file in the same folder
        df.to_csv(modified_file_original, index=False, sep=";")  # Keep the same delimiter (;)

        print(f"Modified CSV file saved as: {modified_file_original}")



