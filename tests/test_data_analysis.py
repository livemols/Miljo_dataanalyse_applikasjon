import sys
import pandas as pd
import os 
import unittest
import numpy as np
from statistics import mode
import matplotlib.dates as mdates
import datetime as datetime


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class test_data_analysis(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "Snø": [0.3,0.5,0.5,0,2,3,0,0,0.5,0.5,0.4,0,1,0], #(3-2-3)
            "Nedbør": [0,1,1,2,4,0,1,1,1,5,0,1,3,0], #(4-4-2)
        })


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



if __name__ == "__main__":
    unittest.main()