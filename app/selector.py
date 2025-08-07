"""
Author: Henry X
Date: 2025/8/5 20:57
File: selector.py
Description: [Add your description here]
"""

from services.search import search_papers
from services.selection import list_topics, load_selected, save_selected
from utils.plot import categoryYear_pie
from utils.plot import advice
import gradio as gr
from typing import List



def build_selector_ui(topic_state, papers_state, selected_urls, paper_lookup):

    def _choices(mode: str):
        if mode == "avail":
            return [
                (p['title'][:80], p['url'])
                for p in papers_state.value
                if p["url"] not in selected_urls.value
            ]
        else:
            return [
                (paper_lookup.value[u]['title'][:80], u)
                for u in selected_urls.value
                if u in paper_lookup.value
            ]

    def _table(urls: List[str]):
        rows = []
        for url in urls:
            p = paper_lookup.value.get(url)
            if not p:
                continue
            authors = ", ".join(a.get("name", "") for a in p.get("authors", []))
            markdown_link = f"[url]({url})"
            row = [
                p.get("title", ""),
                authors,
                p.get("venue", ""),
                p.get("year", ""),
                p.get("citationCount", 0),
                markdown_link,
            ]
            rows.append(row)
        return rows or [["No results", "", "", "", 0, ""]]

    with gr.Column():
        with gr.Row():
            raw_topics = list_topics()
            choices = raw_topics + ["⨁ New…"]
            topic_value = str(topic_state.value) if topic_state.value in choices else "⨁ New…"

            topic_dd = gr.Dropdown(label="Topic", choices=choices, value=topic_value)
            new_topic = gr.Textbox(visible=(topic_value == "⨁ New…"))
            create_bt = gr.Button("Create", visible=(topic_value == "⨁ New…"))

        with gr.Row():
            query_in = gr.Textbox(label="Semantic Scholar query")
            search_bt = gr.Button("Search")

        with gr.Row():
            with gr.Column(scale=5):
                gr.Markdown("### 🔍 Available Papers")
                add_dd = gr.Dropdown(multiselect=True, label="Add")
                add_btn = gr.Button("➕ Add")
                avail_table = gr.Dataframe(
                    headers=["Title", "Authors", "Venue", "Year", "Citations", "URL"],
                    datatype=["str", "str", "str", "number", "number", "markdown"],
                    interactive=False,
                    wrap=True
                )
            with gr.Column(scale=5):
                gr.Markdown("### ✅ Selected Papers")
                rem_dd = gr.Dropdown(multiselect=True, label="Remove")
                rem_btn = gr.Button("❌ Remove")
                sel_table = gr.Dataframe(
                    headers=["Title", "Authors", "Venue", "Year", "Citations", "URL"],
                    datatype=["str", "str", "str", "number", "number", "markdown"],
                    interactive=False,
                    wrap=True
                )

        metric = gr.Markdown()
        chart_im = gr.Image(height=250)
        sugg_md = gr.Markdown()

        def refresh():
            left = _table([p["url"] for p in papers_state.value if p["url"] not in selected_urls.value])
            right = _table(selected_urls.value)
            stat = f"**Selected:** {len(selected_urls.value)}"
            chart = categoryYear_pie([paper_lookup.value[u] for u in selected_urls.value if u in paper_lookup.value])
            hint = advice([paper_lookup.value[u] for u in selected_urls.value if u in paper_lookup.value])

            return (
                gr.update(value=left),
                gr.update(value=right),
                stat,
                gr.update(choices=_choices("avail"), value=[]),
                gr.update(choices=_choices("sel"), value=[]),
                chart, hint,
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(choices=list_topics() + ["⨁ New…"], value=topic_state.value),
            )

        def on_topic(sel):
            topic_state.value = sel
            if sel == "⨁ New…":
                return (
                    gr.update(value=[]), gr.update(value=[]), metric.value,
                    gr.update(value=[]), gr.update(value=[]),
                    chart_im.value, sugg_md.value,
                    gr.update(visible=True), gr.update(visible=True),
                    gr.update(choices=list_topics() + ["⨁ New…"], value=sel),
                )
            papers_state.value = load_selected(sel)
            selected_urls.value = [p["url"] for p in load_selected(sel)]
            paper_lookup.value = {p["url"]: p for p in papers_state.value}
            return refresh()

        def on_create(name):
            name = name.strip()
            if not name:
                return gr.Warning("Topic name required")
            if name not in list_topics():
                save_selected(name, [])
            topic_state.value = name
            return on_topic(name)

        def on_search(q):
            new_papers = search_papers(q)
            papers_state.value = new_papers
            old_selected_papers = [paper_lookup.value[u] for u in selected_urls.value if u in paper_lookup.value]
            merged = {p["url"]: p for p in old_selected_papers + new_papers}
            paper_lookup.value = merged
            return refresh()

        def on_add(urls):
            for url in urls or []:
                if url not in selected_urls.value:
                    selected_urls.value.append(url)
            save_selected(topic_state.value, [paper_lookup.value[u] for u in selected_urls.value if u in paper_lookup.value])
            return refresh()

        def on_remove(urls):
            for url in urls or []:
                if url in selected_urls.value:
                    selected_urls.value.remove(url)
            save_selected(topic_state.value, [paper_lookup.value[u] for u in selected_urls.value if u in paper_lookup.value])
            return refresh()

        SEARCH_OUTPUTS = [
            avail_table, sel_table, metric,
            add_dd, rem_dd, chart_im, sugg_md,
            new_topic, create_bt, topic_dd
        ]

        topic_dd.change(on_topic, topic_dd, outputs=SEARCH_OUTPUTS)
        create_bt.click(on_create, new_topic, outputs=SEARCH_OUTPUTS)
        search_bt.click(on_search, query_in, outputs=SEARCH_OUTPUTS)
        add_btn.click(on_add, add_dd, outputs=SEARCH_OUTPUTS)
        rem_btn.click(on_remove, rem_dd, outputs=SEARCH_OUTPUTS)

        refresh()










