import openai
import gradio
from dotenv import load_dotenv
from os import getenv

load_dotenv()
openai.api_key = getenv('GPT4FREE_API_KEY')
openai.api_base = getenv('GPT4FREE_API_BASE')

with open("assets/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()
messages = []
def generate(prompt, history = []):
    global messages
    messages = messages[-5:]

    messages.append(
        {"role": "user", "content": prompt}
    )
    response = chat_completion = openai.ChatCompletion.create(
        stream=True,
        model='gpt-3.5-turbo',
        messages=messages
    )
    history += [[prompt, None]]
    history[-1][1] = ''
    result = ""
    for trunk in response:
        content = trunk['choices'][0]['delta'].get('content')
        if content != None:
            result += content
            history[-1][1] += content
            yield '', history

    messages.append(
        {"role": "assistant", "content": result}
    )

with gradio.Blocks(title = 'AI问答助手', css=customCSS, theme = gradio.themes.Soft(primary_hue=gradio.themes.colors.blue)) as X:
    gradio.Markdown("## AI问答助手")
    chatbot = gradio.Chatbot(elem_id="chatbot").style(height=500)
    msg = gradio.Textbox(show_label=False, placeholder="请输入您的问题")

    msg.submit(generate, [msg, chatbot], [msg, chatbot])

X.queue().launch(server_name='0.0.0.0', server_port=8001 ,inbrowser=True)
