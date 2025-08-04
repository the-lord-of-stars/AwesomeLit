import os
from dotenv import load_dotenv

load_dotenv()

# Create a global variable for each environment variable
S2_API_KEY = os.getenv("S2_API_KEY")