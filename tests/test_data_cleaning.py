import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'src')))

class TestCleaning(unittest.TestCase):
    def test_function():


suite = unittest.TestLoader().loadTestsFromTestCase(TestMathOperations)

unittest.TextTestRunner().run(suite)
