import os
import sys 
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


#read the right files from the right folders
base_dir = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(base_dir, "..", "..", "data"))
original_file = "blindern_data_cleaning.csv"
original_path = os.path.join(data_path, original_file)

df = pd.read_csv(original_path, delimiter=";")
src_path = os.path.abspath(os.path.join(base_dir, "..", "..", "src"))
sys.path.insert(0, src_path)

from data_preparation.data_cleaning import DataCleaning


class MissingValues:
    def make_dataframe(self,data_type,frac_missing=0.35):
        df_data = df[["Tid",data_type]].head(200)

        df_NaN = df_data.copy()
        sampled_index = df_NaN.sample(frac=frac_missing).index
        df_NaN.loc[sampled_index, data_type] = np.nan

        df_clean = df_NaN.copy()
        data_cleaner = DataCleaning(df_clean)
        df_clean = data_cleaner.replacing().df

        return df_data, df_clean

    def measured_calculated_plot(self,data_type,frac_missing=0.35):
        df_data, df_clean = self.make_dataframe(data_type,frac_missing)

        fig,ax = plt.subplots()

        df_data[data_type].plot(ax=ax,label="Målt data",color="green")
        df_clean[data_type].plot(ax=ax,label="Utregnet data",color="blue")
        
        ax.set_title(f"{data_type} over tid")
        ax.set_ylabel("Verdi")
        ax.set_xlabel("Dag")
        plt.legend()
        plt.show()

    def table(self,data_type,frac_missing=0.35):
        df_data, df_clean = self.make_dataframe(data_type,frac_missing)
        
        des_data = df_data[data_type].describe().round(2)
        des_clean = df_clean[data_type].describe().round(2)
        difference = (des_data - des_clean).round(2)

        original_col = f"{data_type} (Original)"
        cleaned_col = f"{data_type} (Utregnet)"
        diff_col = f"{data_type} (Differanse)"

        summary = pd.concat([
            des_data.rename(f"{data_type} (Original)"),
            des_clean.rename(f"{data_type} (Utrgnet)"),
            difference.rename(f"{data_type} (Differanse)"),],axis=1)

        return summary
