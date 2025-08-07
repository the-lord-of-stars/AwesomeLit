"""
Author: Henry X
Date: 2025/8/4 20:48
File: main.py
Description: This is the GUI of the Literature Review tool.
"""

from app.ui import build_ui

if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="127.0.0.1", server_port=7860)
