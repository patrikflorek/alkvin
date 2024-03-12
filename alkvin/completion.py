import os

import multitasking

from kivy.clock import Clock

from openai import OpenAI


open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@multitasking.task
def generate_completion(instructions, messages, callback):
    completion_messages = [
        {
            "role": message["role"],
            "content": (message["transcript_text"] or message["completion_text"]),
        }
        for message in messages
        if (message["message_sent_at"] or message["completion_received_at"])
    ]
    context = [{"role": "system", "content": instructions}, *completion_messages]
    completion = open_ai_client.chat.completions.create(messages=context, model="gpt-4")

    Clock.schedule_once(lambda dt: callback(completion.choices[0].message.content))
