import os

import multitasking

from kivy.clock import Clock

import openai
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")

open_ai_client = OpenAI()


LANGUAGE = "sk"


@multitasking.task
def transcribe_audio(audio_path, callback):
    with open(audio_path, "rb") as af:
        transcription = open_ai_client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            language=LANGUAGE,
            response_format="json",
        )

    Clock.schedule_once(lambda dt: callback(transcription.text))
