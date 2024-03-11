import os

import multitasking

from kivy.clock import Clock

from openai import OpenAI


open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@multitasking.task
def generate_speech(text, callback):
    speech_audio = open_ai_client.audio.speech.create(
        input=text,
        voice="shimmer",
        model="tts-1",
        response_format="wav",
    )

    Clock.schedule_once(lambda dt: callback(speech_audio))
