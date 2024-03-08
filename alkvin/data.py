import os
import json
import random
import string

from datetime import datetime


# Models
DEFAULT_TRANSCRIPTION_MODEL = "openai/whisper-1"
DEFAULT_COMPLETION_MODEL = "openai/gpt-3.5-turbo"
DEFAULT_SPEECH_MODEL = "openai/tts-1"

# Chats

CHATS_PATH = os.path.abspath("data/chats/")

DEFAULT_CHAT_TITLE = "New Chat"
DEFAULT_CHAT_SUMMARY = "This is a new chat."

DEFAULT_INSTRUCTIONS = """
You are a language tutor. You communicate with your student using audio messages. You start by generating
a text which is then converted to speech using text-to-speech deep neural model. Your student then listents to the speech and records a respose.
The response is then transcribed to text by speech-to-text deep neural model. The resulting text is then served back to you. You continue by generating another
response and the whole process repeats until student stops to respond. Every time you receive a response from the student, you are charged a fee. The transcript you receive
from the student may contain many errors and you should take that into account when generating a response.
You should first try to guess what the intended message was and then generate a response.
"""


def load_chat_list_items():
    """Return a list of chat items with the chat id, title, summary, creation time etc."""

    chat_list_items = []

    chat_dirs = [
        file
        for file in os.listdir(CHATS_PATH)
        if os.path.isdir(os.path.join(CHATS_PATH, file))
    ]
    for chat_dir in chat_dirs:
        chat_json_path = os.path.join(CHATS_PATH, chat_dir, "chat.json")
        with open(chat_json_path) as f:
            chat_data = json.load(f)

        chat_list_items.append(chat_data)

    chat_list_items.sort(key=lambda d: d["chat_created_at"], reverse=True)

    return chat_list_items


def get_new_chat_id():
    """Return a chat name which is 12 characters long random alphanumeric string."""

    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


def create_chat(chat_id):
    """Create a new chat with the given name. Raises an error if the chat already exists."""

    os.makedirs(os.path.join(CHATS_PATH, chat_id))

    # Creation time of the directory is creation time of the chat

    created_at_timestamp = os.path.getctime(os.path.join(CHATS_PATH, chat_id))
    created_at = datetime.fromtimestamp(created_at_timestamp).isoformat()

    with open(os.path.join(CHATS_PATH, chat_id, "chat.json"), "w") as f:
        json.dump(
            {
                "chat_id": chat_id,
                "chat_title": DEFAULT_CHAT_TITLE,
                "chat_summary": DEFAULT_CHAT_SUMMARY,
                "chat_created_at": created_at,
                "chat_modified_at": created_at,
                "transcription_model": DEFAULT_TRANSCRIPTION_MODEL,
                "completion_model": DEFAULT_COMPLETION_MODEL,
                "speech_model": DEFAULT_SPEECH_MODEL,
                "instructions": DEFAULT_INSTRUCTIONS,
            },
            f,
        )

    with open(os.path.join(CHATS_PATH, chat_id, "messages.json"), "w") as f:
        json.dump([], f)


def load_chat(chat_id):
    with open(os.path.join(CHATS_PATH, chat_id, "chat.json")) as f:
        chat_data = json.load(f)

    return chat_data


# Messages


def create_message(chat_id, **message_data):
    return {
        "chat_id": chat_id,
        "role": message_data["role"],
        "user_audio_file": message_data.get("user_audio_file", ""),
        "user_audio_created_at": message_data.get("user_audio_created_at", ""),
        "message_sent_at": message_data.get("message_sent_at", ""),
        "transcript_text": message_data.get("transcript_text", ""),
        "transcript_received_at": message_data.get("transcript_received_at", ""),
        "transcript_price": message_data.get("transcript_price", ""),
        "completion_text": message_data.get("completion_text", ""),
        "completion_received_at": message_data.get("completion_received_at", ""),
        "completion_price": message_data.get("completion_price", ""),
        "speech_audio_file": message_data.get("speech_audio_file", ""),
        "speech_audio_received_at": message_data.get("speech_audio_received_at", ""),
        "speech_audio_price": message_data.get("speech_audio_price", ""),
    }


def load_messages(chat_id):

    def sent_key(message):
        if message["role"] == "user" and not message["message_sent_at"]:
            return (1, message["message_sent_at"])

        return (0, message["message_sent_at"] or message["completion_received_at"])

    with open(os.path.join(CHATS_PATH, chat_id, "messages.json")) as f:
        messages_data = json.load(f)

    messages_with_chat_id = list(
        map(lambda d: create_message(chat_id, **d), messages_data)
    )
    messages_with_chat_id.sort(key=sent_key)

    return messages_with_chat_id


def save_messages(chat_id, messages):
    """Create a new message in the given chat with the given audio frames."""
    messages_path = os.path.join(CHATS_PATH, chat_id, "messages.json")
    clean_messages = list(
        map(lambda d: {k: v for k, v in d.items() if k != "chat_id"}, messages)
    )

    with open(messages_path, "w") as f:
        json.dump(clean_messages, f)


# Audio


def get_new_audio_filename():
    """Return a audio name which is 12 characters long random alphanumeric string."""
    new_audio_filename = (
        "".join(random.choices(string.ascii_letters + string.digits, k=12)) + ".wav"
    )

    return new_audio_filename


def get_audio_path(chat_id, audio_filename):
    """Return the path to the audio file in the given chat."""

    return os.path.join(CHATS_PATH, chat_id, audio_filename)
