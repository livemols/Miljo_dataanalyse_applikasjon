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
from modelling.predictive_analysis import PredictiveAnalysis

class TestPredictiveAnalysis(unittest.TestCase):   #ChatGPT helped with structure as well as the overall ideas
    def setUp(self):
        # DataFrame similar to the original 
        self.df = pd.DataFrame({
            'Tid': pd.date_range(start='2020-01-01', periods=5, freq='D'),
            'Middeltemp': [1.0, 2.5, 3.2, 4.1, 5.0],
            'Snø': [0, 0, 1, 0, 2],
            'KonstantKolonne': [1, 1, 1, 1, 1]
        })
        self.pa = PredictiveAnalysis()

    def test_managing_categorial_data(self):
        df_mod = self.pa.managing_categorial_data(self.df)
        # Check that 'Time' is removed
        self.assertNotIn('Tid', df_mod.columns)
        # Check that 'Tid_num', 'År', 'Måned' exists 
        self.assertIn('Tid_num', df_mod.columns)
        self.assertIn('År', df_mod.columns)
        self.assertIn('Måned', df_mod.columns)
        # Konstant column will be removed
        self.assertNotIn('KonstantKolonne', df_mod.columns)
        # Check that the length of the DataFrame is unchanged
        self.assertEqual(len(df_mod), len(self.df))

    def test_pred_amount_over_limits(self):
        # Make input x, y
        X = pd.DataFrame({'Tid': np.arange(10)})
        y = pd.DataFrame({
            'Middeltemp': np.linspace(10, 20, 10),
            'Snø': np.linspace(0, 5, 10)
        })
        results = self.pa.pred_amount_over_limits(X, y)
        # Check that the result is dict and has the same ammout of keys as the y-column
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), y.shape[1])
        # check that each key contains the expected keys
        for key in results:
            self.assertIn('model', results[key])
            self.assertIn('predictions', results[key])
            self.assertIn('mse', results[key])
            self.assertIn('y_test', results[key])
            self.assertIn('coefficients', results[key])
        # Check that model coefficients have expected length 
        for key in results:
            self.assertEqual(len(results[key]['coefficients']), 1)

if __name__ == '__main__':
    unittest.main()
