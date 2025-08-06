"""
Author: Henry X
Date: 2025/8/5 20:43
File: plot.py
Description: [Add your description here]
"""

from collections import Counter
from io import BytesIO
from PIL import Image
from typing import List, Dict
import matplotlib.pyplot as plt


def category_pie(selected):
    if not selected:
        return None
    cats = [p.get("category", "Unknown") for p in selected]
    sizes = Counter(cats)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes.values(), labels=sizes.keys(), autopct="%1.0f%%", startangle=90)
    ax.axis("equal")

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=120)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

def advice(selected: List[Dict]) -> str:
    if not selected:
        return "⚠️ No papers selected."
    cats = [p.get("category", "Unknown") for p in selected]
    major, cnt = Counter(cats).most_common(1)[0]
    share = cnt / len(cats)
    if share > 0.7:
        return f"🔎 '{major}' dominates {share:.0%}. Consider diversifying years."
    return "✅ Year distribution looks balanced."

