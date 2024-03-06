import os

import multitasking

from kivy.clock import Clock

from openai import OpenAI


open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


LANGUAGE = "en"


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
