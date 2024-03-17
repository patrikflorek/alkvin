import os
import json
import random
import string
import shutil

from datetime import datetime


# Chats

CHATS_PATH = os.path.abspath("data/chats/")

DEFAULT_CHAT_TITLE = "New Chat"
DEFAULT_CHAT_SUMMARY = "This is a new chat."


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
            },
            f,
            indent=2,
        )

    with open(os.path.join(CHATS_PATH, chat_id, "messages.json"), "w") as f:
        json.dump([], f)


def load_chat(chat_id):
    with open(os.path.join(CHATS_PATH, chat_id, "chat.json")) as f:
        chat_data = json.load(f)

    return chat_data


def save_chat(chat):
    chat_id = chat["chat_id"]
    chat_path = os.path.join(CHATS_PATH, chat_id, "chat.json")

    with open(chat_path, "w") as f:
        json.dump(chat, f, indent=2)


def delete_chat(chat_id):
    """Delete the chat with given id."""

    chat_path = os.path.join(CHATS_PATH, chat_id)
    shutil.rmtree(chat_path)


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
        json.dump(clean_messages, f, indent=2)


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


# Robots

ROBOTS_PATH = os.path.abspath("data/robots/")

ROBOT_DEFAULT_FILE = "dummybot.json"

ROBOT_DEFAULT_LANGUAGE = "en"
ROBOT_DEFAULT_SPEECH_TO_TEXT_MODEL = "whisper-1"
ROBOT_DEFAULT_SPEECH_TO_TEXT_PROMPT = "Transcribe the following audio."
ROBOT_DEFAULT_TEXT_GENERATION_MODEL = "gpt-3.5-turbo"
ROBOT_DEFAULT_INSTRUCTIONS_PROMPT = "Respond whatever you think is appropriate."
ROBOT_DEFAULT_SUMMARIZATION_PROMPT = "Generate a title and a short summary (about 50 words) of the conversation so far. Return them in JSON format with keys 'title' and 'summary'."
ROBOT_DEFAULT_TEXT_TO_SPEECH_MODEL = "tts-1"


def load_robot_list_items():
    """Return a list of robot items with the robot id, name, description etc."""

    robots_data = []

    robot_files = [
        file
        for file in os.listdir(ROBOTS_PATH)
        if os.path.isfile(os.path.join(ROBOTS_PATH, file))
    ]
    for robot_file in robot_files:
        robot_json_path = os.path.join("data/robots", robot_file)
        with open(robot_json_path) as f:
            robot_data = json.load(f)

        robot_data["robot_file"] = robot_file
        robots_data.append(robot_data)

    robots_data.sort(key=lambda d: d["robot_name"])
    return robots_data


def get_new_robot_file():
    """Return a robot name which is 12 characters long random alphanumeric string."""

    return "".join(random.choices(string.ascii_letters + string.digits, k=12)) + ".json"


def robot_file_exists(robot_file):
    return os.path.exists(os.path.join(ROBOTS_PATH, robot_file))


def get_default_robot_file():
    return ROBOT_DEFAULT_FILE


def create_robot(robot_file):
    """Create a new robot with the given name. Raises an error if the robot already exists."""

    robot_path = os.path.join(ROBOTS_PATH, robot_file)
    if os.path.exists(robot_path):
        raise ValueError(f"Robot with file {robot_file} already exists.")

    with open(robot_path, "w") as f:
        json.dump(
            {
                "robot_name": "New Robot",
                "robot_description": "This is a new robot.",
                "robot_language": ROBOT_DEFAULT_LANGUAGE,
                "robot_speech_to_text_model": ROBOT_DEFAULT_SPEECH_TO_TEXT_MODEL,
                "robot_speech_to_text_prompt": ROBOT_DEFAULT_SPEECH_TO_TEXT_PROMPT,
                "robot_text_generation_model": ROBOT_DEFAULT_TEXT_GENERATION_MODEL,
                "robot_instructions_prompt": ROBOT_DEFAULT_INSTRUCTIONS_PROMPT,
                "robot_summarization_prompt": ROBOT_DEFAULT_SUMMARIZATION_PROMPT,
                "robot_text_to_speech_model": ROBOT_DEFAULT_TEXT_TO_SPEECH_MODEL,
            },
            f,
            indent=2,
        )


def load_robot(robot_file):
    with open(os.path.join(ROBOTS_PATH, robot_file)) as f:
        robot_data = json.load(f)

    return {
        "robot_file": robot_file,
        "robot_name": robot_data["robot_name"],
        "robot_description": robot_data["robot_description"],
        "robot_language": robot_data.get("robot_language", ROBOT_DEFAULT_LANGUAGE),
        "robot_speech_to_text_model": robot_data.get(
            "robot_speech_to_text_model", ROBOT_DEFAULT_SPEECH_TO_TEXT_MODEL
        ),
        "robot_speech_to_text_prompt": robot_data.get(
            "robot_speech_to_text_prompt", ROBOT_DEFAULT_SPEECH_TO_TEXT_PROMPT
        ),
        "robot_text_generation_model": robot_data.get(
            "robot_text_generation_model", ROBOT_DEFAULT_TEXT_GENERATION_MODEL
        ),
        "robot_instructions_prompt": robot_data.get(
            "robot_instructions_prompt", ROBOT_DEFAULT_INSTRUCTIONS_PROMPT
        ),
        "robot_summarization_prompt": robot_data.get(
            "robot_summarization_prompt", ROBOT_DEFAULT_SUMMARIZATION_PROMPT
        ),
        "robot_text_to_speech_model": robot_data.get(
            "robot_text_to_speech_model", ROBOT_DEFAULT_TEXT_TO_SPEECH_MODEL
        ),
    }


def save_robot(robot):
    robot_file = robot["robot_file"]
    robot_path = os.path.join(ROBOTS_PATH, robot_file)

    robot_data = {k: v for k, v in robot.items() if k != "robot_file"}

    with open(robot_path, "w") as f:
        json.dump(robot_data, f, indent=2)


def delete_robot(robot_file):
    """Delete the robot with given file."""

    robot_path = os.path.join(ROBOTS_PATH, robot_file)
    os.remove(robot_path)
