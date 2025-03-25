import sys
import pandas as pd
import os 
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../sources')))

class test_behandlet_data(unittest.TestCase):

    def setUp(self):
        #oppretter testlisten med én dyplikat
        self.df=pd.DataFrame({
            "Navn": ["Oslo","Oslo","Oslo"],
            "Stasjon": ["SN18700","SN18700","SN18700"],
            "Tid": ["21.02.2025","22.02.2025","22.02.2025"],
            "Makstemp": [7,8,8],
            "Mintemp": [3,4,4],
            "Nedbør": [0,1,1],
            "Vind": [4,2,2],
            "Snø": [0.3,0.5,0.5],
        })
        self.forventede_kolonner = ["Navn","Stasjon","Tid","Makstemp","Mintemp","Nedbør","Vind","Snø"]

        #ser at navnet til kolonnene blir korrekt
    def test_navnendring_kolonner(self):
        df=self.df.copy()
        df.columns=self.forventede_kolonner
        self.assertEqual(list(df.columns),self.forventede_kolonner)
    
        #ser at tiden blir skrevet om korret til Y-M-D i stedet for D-M-Y
    def test_tid_omskriving(self):
        df=self.df.copy()
        df["Tid"] = pd.to_datetime(df["Tid"], format="%d.%m.%Y")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["Tid"]))

    def test_duplikat_fjerning(self):
        df=self.df.copy()
        df.drop_duplicates(inplace = True)
        self.assertEqual(len(df),len(self.df)-1)

if __name__ == "__main__":
    unittest.main()




