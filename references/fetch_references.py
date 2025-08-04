import time
import requests
from typing import List, Dict
from tool.load_envs import S2_API_KEY
from tool.load_config import SEARCH_LIMIT, SEARCH_URL


def fetch_references(query: str) -> List[Dict]:
    """
    Use the Semantic Scholar API to fetch references for a given query.

    Args:
        query (str):

    """
    rsp = requests.get(
        SEARCH_URL,
        headers={"X-API-KEY": S2_API_KEY} if S2_API_KEY else {},
        params={
            "query": query,
            "limit": SEARCH_LIMIT,
            "fields": "title,authors,venue,year,abstract,citationStyles,citationCount",
        },
    )
    print(f"Response Status Code: {rsp.status_code}")
    print(
        f"Response Content: {rsp.text[:100]}"
    )  # Print the first 100 characters of the response content
    rsp.raise_for_status()
    results = rsp.json()
    total = results["total"]
    time.sleep(1.0)
    if not total:
        return None

    papers_info = results["data"]
    return papers_info


# Test the function
if __name__ == "__main__":
    papers = fetch_references(query="deep learning")
    for paper in papers:
        print(paper["title"])