import os
import json
import random
import string


# Chats

CHATS_PATH = "data/chats/"


def load_chat_ids():
    chat_ids = [
        {"chat_id": d}
        for d in os.listdir(CHATS_PATH)
        if os.path.isdir(os.path.join(CHATS_PATH, d))
    ]
    return chat_ids


def get_new_chat_id():
    """Return a chat name which is 12 characters long random alphanumeric string."""

    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


def create_chat(chat_id):
    """Create a new chat with the given name. Raises an error if the chat already exists."""

    os.makedirs(os.path.join(CHATS_PATH, chat_id))
    with open(os.path.join(CHATS_PATH, chat_id, "messages.json"), "w") as f:
        json.dump([], f)


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
        "tts_audio_file": message_data.get("tts_audio_file", ""),
        "tts_audio_received_at": message_data.get("tts_audio_received_at", ""),
        "tts_audio_price": message_data.get("tts_audio_price", ""),
    }


def load_messages(chat_id):
    if not chat_id:
        return []

    with open(os.path.join(CHATS_PATH, chat_id, "messages.json")) as f:
        messages_data = json.load(f)

    return list(map(lambda d: create_message(chat_id, **d), messages_data))


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

    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


def get_audio_path(chat_id, audio_filename):
    """Return the path to the audio file in the given chat."""

    return os.path.join(CHATS_PATH, chat_id, audio_filename)
