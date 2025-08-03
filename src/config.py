import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
load_dotenv()

# Retrieve the OpenAI API key from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")
