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
    topics      = list_topics()
    default_tp  = topics[0] if topics else "⨁ New…"

    # 全局 State
    topic_state  = gr.State(default_tp)
    papers_state = gr.State(load_selected(default_tp))
    sel_ids      = gr.State(list(range(len(papers_state.value))))

    with gr.Blocks(title="Lit Review Suite") as demo:
        with gr.Tab("Select"):
            build_selector_ui(topic_state, papers_state, sel_ids)
    return demo

