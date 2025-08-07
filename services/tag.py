"""
Author: Henry X
Date: 2025/8/5 20:52
File: search.py
Description: The file to tag the references with different classes
"""

from functools import lru_cache
from typing import List, Dict
from api.fetch_references import fetch_references

BUCKET_SIZE = 5      # every 5 years
LOWER_BOUND = 2015   # start from 2015

def _year_bucket(year_val) -> str:
    try:
        y = int(year_val)
    except (TypeError, ValueError):
        return "Unknown"
    if y < LOWER_BOUND:
        return f"≤ {LOWER_BOUND-1}"
    upper = ((y - LOWER_BOUND) // BUCKET_SIZE) * BUCKET_SIZE + LOWER_BOUND + BUCKET_SIZE - 1
    lower = upper - BUCKET_SIZE + 1
    return f"{lower}–{upper}"

@lru_cache(maxsize=32)
def search_papers(query: str, limit: int = 50) -> List[Dict]:
    papers = fetch_references(query=query)
    for p in papers:
        p.setdefault("year", "N/A")
        p["categoryYear"] = _year_bucket(p["year"])
        p.setdefault("citationCount", 0)
        p.setdefault("abstract", "")
    return papers
