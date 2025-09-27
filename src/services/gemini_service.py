import google.generativeai as genai
from src.models.gemini_config import GeminiConfiguration

import logging

logging.basicConfig(level=logging.INFO)

class GeminiService:
    def __init__(self):
        with open(".gemini_api_key", "r") as f:
            api_key = f.read().strip()
        genai.configure(api_key=api_key)

    def generate_content(self, prompt: str) -> str:
        logging.info(f"Generating content for prompt: {prompt}")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        logging.info(f"Generated content: {response.text}")
        return response.text
