import sys
import pandas as pd
import os 
import unittest
import numpy as np
from statistics import mode
import matplotlib.dates as mdates
import datetime as datetime


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modelling.data_analysis import DataAnalysis

class test_data_analysis(unittest.TestCase):
    def setUp(self):
        datoer = np.array(["2020-02-02", "2020-03-02", "2021-05-02", 
                           "2021-07-15", "2022-08-02", "2022-09-02", 
                           "2023-02-01", "2023-10-03", "2024-05-01", 
                           "2024-09-12", "2025-02-01", "2025-03-27", 
                           "2026-11-04", "2026-11-05"])
        self.df = pd.DataFrame({
            "Tid": datoer,
            "Snø": [0.3, 0.5, 0.5, 0, 2, 3, 0, 0, 0.5, 0.5, 0.4, 0, 1, 0],
            "Nedbør": [0, 1, 1, 2, 4, 0, 1, 1, 1, 5, 0, 1, 3, 0],
            "Mintemp": [-5, -10, -7, -12, -3, -6, -8, -11, -4, -9, -10, -7, -6, -5]
        })
        self.da = DataAnalysis()

    def test_season(self):
        def season(dato):
            month=dato.month
            if month in [12,1,2]:
                return "Vinter"
            elif month in [3,4,5]:
                return "Vår"
            elif month in [6,7,8]:
                return "Sommer"
            elif month in [9,10,11]:
                return "Høst"
            
        self.assertEqual(season(datetime.datetime(2023, 1, 15)), "Vinter")
        self.assertEqual(season(datetime.datetime(2022, 12, 15)), "Vinter")
        

        self.assertEqual(season(datetime.datetime(2023, 4, 15)), "Vår")
        self.assertEqual(season(datetime.datetime(2023, 5, 25)), "Vår")    #ChatGPT assisted with translating own logic to code

        self.assertEqual(season(datetime.datetime(2014, 6, 2)), "Sommer")
        self.assertEqual(season(datetime.datetime(2023, 8, 15)), "Sommer")

        self.assertEqual(season(datetime.datetime(2017, 9, 27)), "Høst")
        self.assertEqual(season(datetime.datetime(2020, 10, 15)), "Høst")

    def test_drydays(self):
        df = self.df.copy()
        def dry_days(df):
            limit = 2
            count = 0
            no_rain_days=[]
            for rain in df["Nedbør"]:
                if rain > 0:
                    count += 1
                else:
                    if count >=limit:
                        no_rain_days.append(count)
                    count=0
            if count>=limit:
                no_rain_days.append(count)
            return no_rain_days, mode(no_rain_days)
        
        self.assertEqual(dry_days(df),([4, 4, 2], 4))
    
    def test_snowdays(self):
        df = self.df.copy()
        def snowdays(df):
            count=0
            snowdays = []
            limit = 2
            for snow in df["Snø"]:
                if snow > 0:
                    count += 1
                else:
                    if count >= limit:
                        snowdays.append(count)
                    count=0
            if count >= limit: 
                snowdays.append(count)
            return snowdays, mode(snowdays)

        self.assertEqual(snowdays(df),([3, 2, 3], 3))
    
    def test_years_max(self):
        result = self.da.years_max(self.df)
        self.assertEqual(result.loc[2020, "Mintemp"], -10.0, "Gir ikke min-verdi for Mintemp") 
        self.assertEqual(result.loc[2020, "Snø"], 0.5, "Gir ikke max-verdi") 

    def test_years_severity(self):
        limits = {"Mintemp": -9, "Snø": 25}
        result_df, updated_limits = self.da.years_severity(self.df, limits)

        self.assertLessEqual(updated_limits["Mintemp"], -9.0, "Beholdt ikke gitt grense")
        self.assertIn("Nedbør", updated_limits, "Nye grenser ble ikke opprettet for kategorier uten gitt grense")
        self.assertEqual(updated_limits["Nedbør"], 2.5, "Ikke riktig beregnet grense")

        # Hvis indeksen er datetime eller string, gjør om til årstall som int
        if not pd.api.types.is_integer_dtype(result_df.index):
            result_df.index = result_df.index.year if hasattr(result_df.index, 'year') else result_df.index.astype(str).str[:4].astype(int)

        # Sorter indeksen igjen for å holde orden
        result_df = result_df.set_index("Tid")

        # Så kan du trygt gjøre testen:
        self.assertEqual(result_df.loc[2023, "Mintemp"], 1, "Teller ikke overskridelse av grense")




if __name__ == "__main__":
    unittest.main()