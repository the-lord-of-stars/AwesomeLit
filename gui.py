import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("## AwesomeLit")
    with gr.Tab("References Selection"):
        # options
        num_ideas = gr.Textbox(label="Topic: ", value="Put your ideas here")
        btn = gr.Button("Search")

        # Button Logic
        btn.click()


    with gr.Tab("writeup"):
        gr.Markdown("**Not Available**")
    with gr.Tab("review"):
        gr.Markdown("**Not Available**")
    with gr.Tab("report"):
        gr.Markdown("**Not Available**")

demo.launch()