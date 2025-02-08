import unittest
import pandas as pd
from unittest.mock import patch
from src.dataviz.chat import DataChatbot  

class TestDataChatbot(unittest.TestCase):
    def setUp(self):
        # Mock API key for testing
        self.api_key = 'test_api_key'
        
        # Create a sample DataFrame for testing
        self.test_df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [50000, 60000, 75000]
        })

    @patch('anthropic.Anthropic')
    def test_generate_visualization_code_error_handling(self, mock_anthropic):
        # Simulate an error in API call
        mock_anthropic.return_value.messages.create.side_effect = Exception("API Error")

        chatbot = DataChatbot(self.api_key)
            
        with self.assertRaises(Exception):
            chatbot.generate_visualization_code(self.test_df, "Create a plot")

    def test_dataframe_preprocessing(self):
        # Test that DataFrame preprocessing works correctly
        DataChatbot(self.api_key)
            
        # Verify column information extraction
        self.assertTrue(len(self.test_df.columns) > 0)
        self.assertIn('name', self.test_df.columns)
        self.assertIn('age', self.test_df.columns)
        self.assertIn('salary', self.test_df.columns)

    

def main():
    unittest.main()

if __name__ == '__main__':
    main()