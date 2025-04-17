import sys
import pandas as pd
import os 
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class test_behandlet_data(unittest.TestCase):

    def setUp(self):
        dates = pd.date_range("20250301", periods=31) # Kladd til videre arbeid
        df = pd.DataFrame(np.random.randn(len(dates),4), index=dates, columns=["A", "B", "C", "D"])