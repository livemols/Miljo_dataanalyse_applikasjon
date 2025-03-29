import sys
import pandas as pd
import os 
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sources')))

class test_behandlet_data(unittest.TestCase):

    def setUp(self):
        #oppretter testlisten med én dyplikat
        self.df = pd.DataFrame({
            "Navn": ["Oslo","Oslo","Oslo","Oslo"],
            "Stasjon": ["SN18700","SN18700","SN18700","SN18700"],
            "Tid": ["21.02.2025","22.02.2025","22.02.2025","22.02.2025"],
            "Makstemp": [7,8,8,500],
            "Mintemp": [3,4,4,-200],
            "Nedbør": [0,1,1,2],
            "Vind": [4,2,2,np.nan],
            "Snø": [0.3,0.5,0.5,np.nan],
        })
        self.forventede_kolonner = ["Navn","Stasjon","Tid","Makstemp","Mintemp","Nedbør","Vind","Snø"]

        #ser at navnet til kolonnene blir korrekt
    def test_navnendring_kolonner(self):
        df = self.df.copy()
        df.columns=self.forventede_kolonner
        self.assertEqual(list(df.columns),self.forventede_kolonner)
    
        #ser at tiden blir skrevet om korret til Y-M-D i stedet for D-M-Y
    def test_tid_omskriving(self):
        df = self.df.copy()
        df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["Tid"]))

    def test_duplikat_fjerning(self):
        df = self.df.copy()
        df.drop_duplicates(inplace = True)
        self.assertEqual(len(df),(len(self.df)-1))

    def test_outlier_removal(self):
        df = self.df.copy()

        threshold = 3

        for column in df.select_dtypes(include=['number']).columns:
            mean = df[column].mean()
            std = df[column].std()
            lower_limit = mean - threshold * std
            upper_limit = mean + threshold * std

             # ".where" for å beholde NaN i stedet for å fjerne verdier helt
            df[column] = df[column].where(df[column].between(lower_limit, upper_limit))

            self.assertTrue(df[column].dropna().between(lower_limit, upper_limit).all(), f"Outliers found in {column}")


    def test_time_series_data_processing(self): 
        
        df = self.df.copy()


        for column in df.select_dtypes(include=['number']).columns:
            if column in ["Makstemp", "Mintemp"]:
                df[column] = df[column].interpolate(method='polynomial', order=2).round(1)
            if column in ["Nedbør", "Vind", "Snø"]:
                df[column] = df[column].interpolate(method='linear').round(1)
                df[column] = df[column].clip(lower = 0)

                self.assertTrue((df[column] >= 0).all(), f"Negative values found in {column}")

        self.assertEqual(df.isna().sum().sum(), 0, "NaN is still existing in DataFrame")



if __name__ == "__main__":
    unittest.main()




