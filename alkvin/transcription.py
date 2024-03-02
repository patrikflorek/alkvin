import os

import openai
from openai import AsyncOpenAI

openai.api_key = os.getenv("OPENAI_API_KEY")

open_ai_async_client = AsyncOpenAI()


LANGUAGE = "sk"


async def transcribe_audio(audio_path):
    with open(audio_path, "rb") as af:
        transcription = await open_ai_async_client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            language=LANGUAGE,
            response_format="json",
        )

    return transcription
