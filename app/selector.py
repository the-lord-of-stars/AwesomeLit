"""
Author: Henry X
Date: 2025/8/5 20:57
File: selector.py
Description: [Add your description here]
"""

import gradio as gr
from typing import List
from services.search import search_papers
from services.selection import list_topics, load_selected, save_selected
from utils.cards import make_card
from utils.plot import category_pie
from utils.plot import advice

def build_selector_ui(topic_state: gr.State,
                      papers_state: gr.State,
                      selected_ids: gr.State):

    def _choices():
        return [f"{i}: {p['title'][:80]}…" for i, p in enumerate(papers_state.value)]

    def _md(ids: List[int]):
        if not ids:
            return "*None*"
        return "\n\n---\n\n".join(make_card(papers_state.value[i]) for i in ids)

    with gr.Column() as container:
        # ───── 顶栏 Topic ─────
        with gr.Row():
            raw_topics = list_topics()
            choices = raw_topics + ["⨁ New…"]
            state_value = str(topic_state.value) if topic_state.value is not None else None

            if state_value in choices:
                topic_value = state_value
            elif raw_topics:
                topic_value = raw_topics[0]
            else:
                topic_value = "⨁ New…"

            topic_dd = gr.Dropdown(
                label="Topic",
                choices=choices,
                value="⨁ New…",
            )

            new_topic = gr.Textbox(visible=(topic_value == "⨁ New…"))
            create_bt = gr.Button("Create", visible=(topic_value == "⨁ New…"))

        # ───── 搜索栏 ─────
        with gr.Row():
            query_in = gr.Textbox(label="Semantic Scholar query")
            search_bt = gr.Button("Search")

        # ───── 左右列 ─────
        with gr.Row():
            with gr.Column(scale=5):
                gr.Markdown("### 🔍 Available Papers")
                add_dd = gr.Dropdown(multiselect=True)
                add_btn = gr.Button("➕ Add")
                avail_md = gr.Markdown()
            with gr.Column(scale=5):
                gr.Markdown("### ✅ Selected Papers")
                rem_dd = gr.Dropdown(multiselect=True)
                rem_btn = gr.Button("❌ Remove")
                sel_md = gr.Markdown()

        metric   = gr.Markdown()
        chart_im = gr.Image(height=250)
        sugg_md  = gr.Markdown()

    # ───── 刷新展示区 ─────
    def refresh():
        left   = _md([i for i in range(len(papers_state.value)) if i not in selected_ids.value])
        right  = _md(selected_ids.value)
        stat   = f"**Selected:** {len(selected_ids.value)} / {len(papers_state.value)}"
        chart  = category_pie([papers_state.value[i] for i in selected_ids.value])
        hint   = advice([papers_state.value[i] for i in selected_ids.value])

        return (left, right, stat,
                gr.update(choices=_choices(), value=[]),
                gr.update(choices=_choices(), value=[]),
                chart, hint,
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(choices=list_topics() + ["⨁ New…"], value=topic_state.value))

    # ───── 处理选择 topic 的逻辑 ─────
    def on_topic(sel):
        topic_state.value = sel
        if sel == "⨁ New…":
            return (avail_md.value, sel_md.value, metric.value,
                    gr.update(value=[]), gr.update(value=[]),
                    chart_im.value, sugg_md.value,
                    gr.update(visible=True),
                    gr.update(visible=True),
                    gr.update(choices=list_topics() + ["⨁ New…"], value=sel))
        papers_state.value = load_selected(sel)
        selected_ids.value = list(range(len(papers_state.value)))
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
        papers_state.value, selected_ids.value = search_papers(q), selected_ids.value
        save_selected(topic_state.value, [])
        return refresh()

    def on_add(vals):
        for v in vals or []:
            idx = int(v.split(":")[0])
            if idx not in selected_ids.value:
                selected_ids.value.append(idx)
        save_selected(topic_state.value, [papers_state.value[i] for i in selected_ids.value])
        return refresh()

    def on_remove(vals):
        for v in vals or []:
            idx = int(v.split(":")[0])
            if idx in selected_ids.value:
                selected_ids.value.remove(idx)
        save_selected(topic_state.value, [papers_state.value[i] for i in selected_ids.value])
        return refresh()

    SEARCH_OUTPUTS = [avail_md, sel_md, metric,
                      add_dd, rem_dd, chart_im, sugg_md,
                      new_topic, create_bt, topic_dd]

    topic_dd.change(on_topic, topic_dd, outputs=SEARCH_OUTPUTS)
    create_bt.click(on_create, new_topic, outputs=SEARCH_OUTPUTS)
    search_bt.click(on_search, query_in, outputs=SEARCH_OUTPUTS)
    add_btn.click(on_add, add_dd, outputs=SEARCH_OUTPUTS)
    rem_btn.click(on_remove, rem_dd, outputs=SEARCH_OUTPUTS)

    # 初始化同步 state
    topic_state.value = topic_value
    if topic_value != "⨁ New…":
        papers_state.value = load_selected(topic_value)
        selected_ids.value = list(range(len(papers_state.value)))

    refresh()








