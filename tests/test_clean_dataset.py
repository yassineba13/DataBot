import unittest
import pandas as pd
import numpy as np
import warnings
from src.dataviz.utils import clean_dataset

class TestDatasetCleaning(unittest.TestCase):
    def setUp(self):
        self.test_df = pd.DataFrame({
            'User Name': ['John', 'Jane', 'John', None, 'Bob'],
            'Age': [25, np.nan, 25, 100, 30],
            'Score': [10, 20, 10, 1000, -500]
        })

    def test_clean_dataset(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=UserWarning)
            cleaned_df = clean_dataset(self.test_df)
        
        # Test column name standardization
        self.assertTrue(all(col.islower() and ' ' not in col for col in cleaned_df.columns))
        
        # Test duplicate removal
        self.assertEqual(len(cleaned_df), len(self.test_df) - 1)
        
        # Test missing value handling
        self.assertFalse(cleaned_df['user_name'].isna().any())
        self.assertFalse(cleaned_df['age'].isna().any())
        
        # Test data type conversion
        self.assertTrue(np.issubdtype(cleaned_df['age'].dtype, np.number))
        
        # Test outlier handling
        self.assertTrue(cleaned_df['score'].max() <= 1000)
        self.assertTrue(cleaned_df['score'].min() >= -500)

if __name__ == '__main__':
    unittest.main()
