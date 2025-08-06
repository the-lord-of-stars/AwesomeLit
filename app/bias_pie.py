"""
Author: Henry X
Date: 2025/8/5 20:56
File: bias_pie.py
Description: [Add your description here]
"""

import gradio as gr
from utils.plot import category_pie, advice

def build_bias_ui(papers_state: gr.State, selected_ids: gr.State):
    with gr.Column():
        gr.Markdown("### 📊 Year Bucket Distribution")
        img = gr.Image(value=lambda: category_pie(
            [papers_state.value[i] for i in selected_ids.value]) if papers_state.value else None)
        tip = gr.Markdown(value=lambda: advice(
            [papers_state.value[i] for i in selected_ids.value]) if papers_state.value else "⚠️ No selection yet.")
