import unittest

from src.models.gemini_config import GeminiConfiguration

class TestGeminiConfig(unittest.TestCase):

    def test_create_gemini_config(self):
        """Test that we can create a GeminiConfiguration object."""
        config = GeminiConfiguration(api_key="test_api_key")
        self.assertEqual(config.api_key, "test_api_key")

if __name__ == '__main__':
    unittest.main()
