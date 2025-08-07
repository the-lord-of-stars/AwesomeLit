"""
Author: Henry X
Date: 2025/8/5 20:58
File: ui.py
Description: [Add your description here]
"""

import gradio as gr
from app.selector       import build_selector_ui
from services.selection import list_topics, load_selected

def build_ui():
    # 全局 State
    default_tp = "⨁ New…"
    topic_state   = gr.State(default_tp)

    # 加载已保存的论文列表
    selected_papers = load_selected(default_tp)
    selected_urls   = gr.State([p["url"] for p in selected_papers])
    papers_state    = gr.State(selected_papers)
    paper_lookup    = gr.State({p["url"]: p for p in selected_papers})

    with gr.Blocks(title="Lit Review Suite") as demo:
        with gr.Tab("Select"):
            build_selector_ui(topic_state, papers_state, selected_urls, paper_lookup)
    return demo


