# This file is a unittest for functions and classe(s) related to predictive analysis
# This file has used ChatGPT (OpenAI) for troubleshooting and explanation of error codes.

import sys
import pandas as pd
import os 
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import pandas as pd
import numpy as np
from modelling.predictive_analysis import PredictiveAnalysis  # juster importsti etter din mappe

class TestPredictiveAnalysis(unittest.TestCase):
    def setUp(self):
        # Eksempel-data som etterligner struktur i din dataframe
        self.df = pd.DataFrame({
            'Tid': pd.date_range(start='2020-01-01', periods=5, freq='D'),
            'Middeltemp': [1.0, 2.5, 3.2, 4.1, 5.0],
            'Snø': [0, 0, 1, 0, 2],
            'KonstantKolonne': [1, 1, 1, 1, 1]  # skal droppes i metoden
        })
        self.pa = PredictiveAnalysis()

    def test_managing_categorial_data(self):
        df_mod = self.pa.managing_categorial_data(self.df)
        # Sjekk at 'Tid' er fjernet
        self.assertNotIn('Tid', df_mod.columns)
        # Sjekk at 'Tid_num', 'År', 'Måned' finnes
        self.assertIn('Tid_num', df_mod.columns)
        self.assertIn('År', df_mod.columns)
        self.assertIn('Måned', df_mod.columns)
        # Konstant kolonne skal være fjernet
        self.assertNotIn('KonstantKolonne', df_mod.columns)
        # Sjekk at lengde på dataframe er uendret
        self.assertEqual(len(df_mod), len(self.df))

    def test_pred_amount_over_limits(self):
        # Lag input X, y
        X = pd.DataFrame({'Tid': np.arange(10)})
        y = pd.DataFrame({
            'Middeltemp': np.linspace(10, 20, 10),
            'Snø': np.linspace(0, 5, 10)
        })
        results = self.pa.pred_amount_over_limits(X, y)
        # Sjekk at resultatet er dict og har like mange nøkler som y-kolonner
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), y.shape[1])
        # Sjekk at hver nøkkel inneholder forventede keys
        for key in results:
            self.assertIn('model', results[key])
            self.assertIn('predictions', results[key])
            self.assertIn('mse', results[key])
            self.assertIn('y_test', results[key])
            self.assertIn('coefficients', results[key])
        # Sjekk at modell-koeffisienter har forventet lengde (siden kun én funksjon)
        for key in results:
            self.assertEqual(len(results[key]['coefficients']), 1)

if __name__ == '__main__':
    unittest.main()
