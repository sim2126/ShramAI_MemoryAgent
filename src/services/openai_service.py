import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

# Configure the generative AI client with the API key
genai.configure(api_key=GEMINI_API_KEY)

# Configuration for the generation to ensure JSON output
generation_config = {
  "response_mime_type": "application/json",
}

def get_structured_completion(prompt: str) -> dict:
    """
    Calls the Google Gemini API to get a structured JSON completion for a given prompt.

    Args:
        prompt (str): The prompt to send to the language model.

    Returns:
        dict: The parsed JSON object from the model's response.
              Returns an empty dict if the response is not valid JSON.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel(
            "gemini-1.5-flash", # A fast and capable model
            generation_config=generation_config
        )
        
        # Generate the content
        response = model.generate_content(prompt)
        
        # The response text should be a JSON string, so we parse it
        if response.text:
            return json.loads(response.text)
        return {}

    except Exception as e:
        print(f"An error occurred while calling Google Gemini API: {e}")
        return {}
