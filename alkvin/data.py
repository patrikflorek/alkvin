import os
import json
import random
import string


CHATS_PATH = "data/chats/"


def load_chat_ids():
    chat_ids = [
        {"chat_id": d}
        for d in os.listdir(CHATS_PATH)
        if os.path.isdir(os.path.join(CHATS_PATH, d))
    ]
    return chat_ids


def load_messages(chat_id):
    if not chat_id:
        return []

    messages = []
    with open(os.path.join(CHATS_PATH, chat_id, "messages.json")) as f:
        messages = json.load(f)
    return messages


def get_new_chat_id():
    """Return a chat name which is 12 characters long random alphanumeric string."""

    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


def get_new_audio_id():
    """Return a audio name which is 12 characters long random alphanumeric string."""

    return "".join(random.choices(string.ascii_letters + string.digits, k=12))


def get_audio_path(chat_id, audio_id):
    """Return the path to the audio file in the given chat."""

    return os.path.join(CHATS_PATH, chat_id, f"{audio_id}.vaw")


def create_chat(chat_id):
    """Create a new chat with the given name. Raises an error if the chat already exists."""

    os.makedirs(os.path.join(CHATS_PATH, chat_id))
    with open(os.path.join(CHATS_PATH, chat_id, "messages.json"), "w") as f:
        json.dump([], f)


def save_messages(chat_id, messages):
    """Create a new message in the given chat with the given audio frames."""
    messages_path = os.path.join(CHATS_PATH, chat_id, "messages.json")
    print("Messages:", messages_path, chat_id, messages)

    with open(messages_path, "w") as f:
        json.dump(messages, f)
