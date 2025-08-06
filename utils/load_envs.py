"""
Author: Henry X
Date: 2025/8/4 20:48
File: load_envs.py
Description: This file is used to load environment variables from.env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Create a global variable for each environment variable
S2_API_KEY = os.getenv("S2_API_KEY")