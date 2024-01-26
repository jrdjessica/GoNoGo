from django.http import HttpResponseRedirect
from django.shortcuts import render
from threading import Thread

from openai import OpenAI
import gradio as gr
import requests
import json
import asyncio

gradio_running = False
messages = [{"role": "system", "content": "You are an event planner"}]


def start_gradio():
    global gradio_running
    if not gradio_running:
        async def async_gradio():
            def CustomChatGPT(user_input):
                messages.append({"role": "user", "content": user_input})
                prompt = "\n".join(
                    [f"{message['role']}: {message['content']}" for message in messages])

                data = {
                    "model": "gpt-3.5-turbo",
                    "messages": messages
                }

                headers = {
                    'Authorization': f'Bearer {"password"}',
                    'Content-Type': 'application/json'
                }

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
                response_json = response.json()

                ChatGPT_reply = response_json['choices'][0]['message']['content']
                messages.append({"role": "assistant", "content": ChatGPT_reply})
                return ChatGPT_reply
            demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Event Planner Pro")
            await demo.launch(inline=False, inbrowser=False, share=True, server_port=7862)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_gradio())
        gradio_running = True

 

def gradio_view(request):
    # Start Gradio in a separate thread
    thread = Thread(target=start_gradio)
    thread.daemon = True
    thread.start()

    return HttpResponseRedirect("http://127.0.0.1:7862/")
