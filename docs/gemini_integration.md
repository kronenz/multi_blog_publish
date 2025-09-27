# Gemini Integration

This document describes how to integrate Google's Gemini AI into the multi-blog publishing platform.

## Configuration

1.  Create a file named `.gemini_api_key` in the root directory of the project.
2.  Add your Gemini API key to this file.

## Usage

Once the API key is configured, you can use the `GeminiService` to generate content.

```python
from src.services.gemini_service import GeminiService

service = GeminiService()
content = service.generate_content("Hello, world!")
print(content)
```
