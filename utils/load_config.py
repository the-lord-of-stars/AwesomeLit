"""
Author: Henry X
Date: 2025/8/4 20:48
File: load_config.py
Description: This file is used to load the config file.
"""

import os
import yaml

# Define paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")

# Load config file
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

MODEL_NAME = config["model_name"]
SEARCH_LIMIT = config["search_limit"]
SEARCH_URL = config["search_url"]