import os
from datetime import datetime

from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, StringProperty

from kivymd.uix.screen import MDScreen


from alkvin.data import (
    load_chat,
    load_messages,
    create_message,
    save_messages,
)

from alkvin.uix.components.chat_bubble import ChatBubbleBox

from alkvin.audio import get_audio_bus

from alkvin.data import get_audio_path

from alkvin.completion import generate_completion


class ChatScreen(MDScreen):
    chat_id = StringProperty()

    chat = DictProperty({"chat_title": ""})

    messages = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._audio_bus = get_audio_bus()
        self._audio_bus.set_on_save_recording_callback(self.on_save_recording)

    def on_pre_enter(self, *args):
        prev_chat_id = self.chat.get("chat_id")

        self.chat = load_chat(self.chat_id)

        messages = load_messages(self.chat_id)
        if not messages:
            self.create_completion_message()
        else:
            self.messages = messages

        if self.chat_id != prev_chat_id:
            self.ids.chat_scroll.scroll_y = 1

    def on_pre_leave(self, *args):
        self._audio_bus.stop()

    def on_messages(self, instance, messages):
        self.ids.chat_box.clear_widgets()
        for message in messages:
            self.ids.chat_box.add_widget(ChatBubbleBox(message))

    def on_save_recording(self, recording_path):
        audio_file = os.path.basename(recording_path)

        audio_created_at_timestamp = os.path.getmtime(recording_path)
        audio_created_at = datetime.fromtimestamp(
            audio_created_at_timestamp
        ).isoformat()

        message = create_message(
            self.chat_id,
            role="user",
            user_audio_file=audio_file,
            user_audio_created_at=audio_created_at,
        )

        self.messages.append(message)
        save_messages(self.chat_id, self.messages)

    def remove_message(self, index):
        self._delete_message_files(self.messages[index])

        del self.messages[index]
        save_messages(self.chat_id, self.messages)

    def change_message_index(self, message, index):
        current_index = self.messages.index(message)
        if current_index == index:
            return

        self.messages.remove(message)
        self.messages.insert(index, message)

        save_messages(self.chat_id, self.messages)

    def _delete_message_files(self, message):
        if message["role"] == "user":
            audio_path = get_audio_path(message["chat_id"], message["user_audio_file"])
            os.remove(audio_path)

    def save_messages(self):
        save_messages(self.chat_id, self.messages)

    def reload_messages(self):
        self.messages = load_messages(self.chat_id)

    def create_completion_message(self):
        generate_completion(
            self.chat["instructions"], self.messages, self._on_completion_create_message
        )

    def _on_completion_create_message(self, completion_text):
        self.messages.append(
            create_message(
                self.chat_id,
                role="assistant",
                completion_text=completion_text,
                completion_received_at=datetime.now().isoformat(),
            )
        )
        save_messages(self.chat_id, self.messages)
        self.reload_messages()


Builder.load_string(
    """
#:import AudioRecorderBox alkvin.uix.components.audio_recorder.AudioRecorderBox


<ChatScreen>:
    name: "chat"
    
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: root.chat['chat_title']
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
            right_action_items: [["dots-vertical", lambda x: None]]
        
        ScrollView:
            id: chat_scroll
            MDBoxLayout:
                id: chat_box
                
                remove_message: lambda bubble_box: root.remove_message(self.children[::-1].index(bubble_box))
                save_messages: lambda: root.save_messages()
                reload_messages: lambda: root.reload_messages()
                create_completion_message: lambda: root.create_completion_message()

                orientation: "vertical"
                adaptive_height: True
                padding: dp(40), dp(100), dp(40), dp(80)
                spacing: dp(20)

        AudioRecorderBox:
            id: audio_recorder
            chat_id: root.chat_id

    AnchorLayout:
        anchor_x: "right"
        anchor_y: "top"
        padding: dp(48), dp(96)        
        MDFloatingActionButton:
            icon: "robot"
            type: "large"
            elevation_normal: 12
            on_release: None
            md_bg_color: [0.2, 0.6, 0.8, 1]
"""
)
