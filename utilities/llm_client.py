from google import genai
import os

class GeminiClient:
    def __init__(self, api_key=None):
        # Use the new Client class
        self.client = genai.Client(api_key=api_key or os.environ.get("GOOGLE_API_KEY"))

    def generate_content(self, prompt):
        # The method call has changed to models.generate_content
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return response.text