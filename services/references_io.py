"""
Author: Henry X
Date: 2025/8/5 20:51
File: selection.py
Description: the io to read and save json file
"""

import json, re
from pathlib import Path
RESULTS_DIR = Path("results")

def _slug(name: str) -> str:
    return re.sub(r"[^\w\-]", "_", name).lower() or "default"

def load_selected(topic: str) -> list:
    p = RESULTS_DIR / _slug(topic) / "selected.json"
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_selected(topic: str, papers: list):
    folder = RESULTS_DIR / _slug(topic)
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "selected.json").open("w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

def list_topics() -> list[str]:
    # List all topics
    return sorted(p.name for p in RESULTS_DIR.iterdir()
                  if (p / "selected.json").exists())


