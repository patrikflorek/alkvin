import os
import json

from datetime import datetime

from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from alkvin.data import (
    load_chat,
    save_chat,
    delete_chat,
    load_messages,
    create_message,
    save_messages,
    get_audio_path,
)

from alkvin.uix.components.chat_bubble import ChatBubbleBox

from alkvin.audio import get_audio_bus

from alkvin.completion import generate_completion


class ChatScreen(MDScreen):
    chat_id = StringProperty()

    chat = DictProperty({"chat_title": "", "chat_summary": ""})

    messages = ListProperty()

    delete_chat_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._audio_bus = get_audio_bus()
        self._audio_bus.set_on_save_recording_callback(self.on_save_recording)

    def on_pre_enter(self, *args):
        print("ChatScreen on_pre_enter", self.chat_id)
        prev_chat_id = self.chat.get("chat_id")

        self.chat = load_chat(self.chat_id)
        self.chat_id = self.chat["chat_id"]

        self.messages = load_messages(self.chat_id)
        if not self.messages:
            self.create_completion_message()

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

    def summarize_chat(self):
        summarization_massage = create_message(
            chat_id=self.chat_id,
            role="system",
            transcript_text="Vytvor názov a krátky súhrn (približne 50 slov) z celej doterajšej konverzácie. \
                             Výsledok vráť v formáte JSON s kľúčmi `title` a `summary`.",
            # transcript_text="Generate a title and a short summary (about 50 words) of the conversation so far. \
            #                  Return them in JSON format with keys 'title' and 'summary'.",
            message_sent_at=datetime.now().isoformat(),
        )
        summarization_messages = self.messages + [summarization_massage]

        generate_completion(
            self.chat["instructions"], summarization_messages, self._on_summarized_chat
        )

    def _on_summarized_chat(self, summary_str):
        summary = json.loads(summary_str)

        self.chat["chat_title"] = summary["title"]
        self.chat["chat_summary"] = summary["summary"]

        self.ids.chat_scroll.scroll_y = 1

        save_chat(self.chat)

    def open_delete_chat_dialog(self):
        if not self.delete_chat_dialog:
            self.delete_chat_dialog = MDDialog(
                title="Delete chat",
                text="Are you sure you want to delete this chat?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.delete_chat_dialog.dismiss(),
                    ),
                    MDFlatButton(
                        text="DELETE",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self._delete_chat(),
                    ),
                ],
            )

        self.delete_chat_dialog.open()

    def _delete_chat(self):
        self.delete_chat_dialog.dismiss()
        delete_chat(self.chat_id)
        self.manager.goto_previous_screen()


Builder.load_string(
    """
#:import AudioRecorderBox alkvin.uix.components.audio_recorder.AudioRecorderBox


<ChatScreen>:
    name: "chat"
    
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: toolbar
            use_overflow: True
            title: root.chat['chat_title']
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
            right_action_items: 
                [
                ["package-variant", lambda x: root.summarize_chat(), "Summarize chat", "Summarize chat"],
                ["message-cog", lambda x: None, "Chat settings", "Chat settings"],
                ["delete", lambda x: root.open_delete_chat_dialog(), "Delete chat", "Delete chat"],
                ]
        
        ScrollView:
            id: chat_scroll
            MDBoxLayout:
                orientation: "vertical"
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True

                MDCard:
                    orientation: "vertical"
                    padding: "24dp"
                    spacing: "12dp"
                    md_bg_color: [.4, .4, .4, .3]
                    radius: [25, 25, 25, 25]
                    elevation: 0
                    adaptive_height: True

                    MDLabel:
                        text: "Summary"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    MDLabel:
                        text: root.chat["chat_summary"]
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDIconButton:
                        icon: "chevron-down"
                        theme_text_color: "Custom"
                        text_color: [0.4, 0.4, 0.4, 0.8]
                        pos_hint: {"center_x": .5}
                        on_release: chat_scroll.scroll_y = 0

                MDBoxLayout:
                    id: chat_box
                    
                    remove_message: lambda bubble_box: root.remove_message(self.children[::-1].index(bubble_box))
                    save_messages: lambda: root.save_messages()
                    reload_messages: lambda: root.reload_messages()
                    create_completion_message: lambda: root.create_completion_message()

                    orientation: "vertical"
                    adaptive_height: True
                    # padding: dp(40)
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
