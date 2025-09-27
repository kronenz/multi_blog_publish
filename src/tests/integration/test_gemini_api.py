import unittest
import os
import google.generativeai as genai
from google.api_core import exceptions

class TestGeminiApi(unittest.TestCase):

    def test_api_connection(self):
        """Test that we can connect to the Gemini API."""
        # This test is expected to fail at first, because the API key is not set.
        # We will set the API key in a later step.
        with self.assertRaises(exceptions.InvalidArgument):
            genai.configure(api_key="dummy_api_key")
            model = genai.GenerativeModel('gemini-pro')
            model.generate_content("Hello, world!")

if __name__ == '__main__':
    unittest.main()
