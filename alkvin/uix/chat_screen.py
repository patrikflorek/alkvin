import os

from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen


from alkvin.data import get_new_audio_id, get_audio_path, load_messages, save_messages


class ChatScreen(MDScreen):
    chat_id = StringProperty()

    messages = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._voice_recording_on = False

        self.ids.audio_recorder.bind(recording=self.on_recording)

    def on_pre_enter(self, *args):
        self.messages = load_messages(self.chat_id)

    def on_recording(self, instance, recording):
        if not recording:
            audio_filename = self._save_recording()

            self.messages.append(
                {
                    "chat_id": self.chat_id,
                    "role": "user",
                    "audio_file": audio_filename,
                    "text": "",
                }
            )
            save_messages(self.chat_id, self.messages)

    def _save_recording(self):
        audio_path = get_audio_path(self.chat_id, get_new_audio_id())
        self.ids.audio_recorder.save(audio_path)

        return os.path.basename(audio_path)


Builder.load_string(
    """
#:import ChatBubble alkvin.uix.components.chats.ChatBubble
#:import AudioRecorderBox alkvin.uix.components.audio_recorder.AudioRecorderBox


<ChatScreen>:
    name: "chat"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: root.chat_id
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
            right_action_items: [["dots-vertical", lambda x: None]]
        
        RecycleView:
            data: root.messages
            viewclass: "ChatBubble"

            RecycleBoxLayout:
                orientation: "vertical"
                default_size: None, None
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                padding: dp(40), dp(96), dp(40), dp(40)
                spacing: dp(20)

        AudioRecorderBox:
            id: audio_recorder
            recording: False

    AnchorLayout:
        anchor_x: "right"
        anchor_y: "top"
        padding: dp(48), dp(96)        
        MDFloatingActionButton:
            icon: "robot"
            type: "large"
            elevation_normal: 12
            on_release: None
            md_bg_color: [.5, .5, 1, 1]

    AnchorLayout:
        anchor_x: "left"
        anchor_y: "bottom"
        padding: dp(48)        
        MDFloatingActionButton:
            icon: "microphone"
            text_color: [0, 1, 0] if audio_recorder.recording else [1, 1, 1]
            type: "large"
            elevation_normal: 12
            on_release: audio_recorder.recording = not audio_recorder.recording
            md_bg_color: [1, .4, .2, 1]
"""
)
