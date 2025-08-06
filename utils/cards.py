"""
Author: Henry X
Date: 2025/8/5 20:50
File: cards.py
Description: [Add your description here]
"""

from typing import Dict, List

def make_card(p: Dict) -> str:
    title = p.get("title", "<no title>")
    year  = p.get("year", "N/A")
    cites = p.get("citationCount", 0)
    abstract = (p.get("abstract") or "_No abstract available_")[:200] + "…"
    return f"**{title}**\\n\\n{year} · Citations: {cites}\\n\\n{abstract}"

def render(papers: List[Dict], sel_ids: List[int]):
    avail = "\\n\\n".join(make_card(p) for i, p in enumerate(papers) if i not in sel_ids) or "*No more papers.*"
    sel   = "\\n\\n".join(make_card(papers[i]) for i in sel_ids) or "*None selected yet.*"
    metric = f"### Selected: {len(sel_ids)}/{len(papers)}"
    return avail, sel, metric
