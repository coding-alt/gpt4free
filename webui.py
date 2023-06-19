import g4f
import gradio

with open("assets/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()

def generate(prompt, history = []):
    response = g4f.ChatCompletion.create(
        stream=True,
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}]
    )
    history += [[prompt, None]]
    history[-1][1] = ''
    for content in response:
        history[-1][1] += content
        yield '', history

with gradio.Blocks(title = 'AI问答助手', css=customCSS, theme = gradio.themes.Soft(primary_hue=gradio.themes.colors.blue)) as X:
    gradio.Markdown("## AI问答助手")
    chatbot = gradio.Chatbot(elem_id="chatbot").style(height=500)
    msg = gradio.Textbox(show_label=False, placeholder="请输入您的问题")

    msg.submit(generate, [msg, chatbot], [msg, chatbot])

X.queue().launch(server_name='0.0.0.0')
