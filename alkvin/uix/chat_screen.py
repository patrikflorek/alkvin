import os
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.screen import MDScreen


from alkvin.data import (
    get_new_audio_filename,
    get_audio_path,
    load_messages,
    create_message,
    save_messages,
)

from alkvin.uix.components.chat_bubble import ChatBubbleBox


class ChatScreen(MDScreen):
    chat_id = StringProperty()

    messages = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._voice_recording_on = False

        self.ids.audio_recorder.bind(recording=self.on_recording)

    def on_pre_enter(self, *args):
        self.messages = load_messages(self.chat_id)

    def on_messages(self, instance, messages):
        self.ids.chat_box.clear_widgets()
        for message in messages:
            self.ids.chat_box.add_widget(ChatBubbleBox(message))

    def on_recording(self, instance, recording):
        if not recording:
            audio_file, audio_created_at = self._save_recording()

            message = create_message(
                self.chat_id,
                role="user",
                user_audio_file=audio_file,
                user_audio_created_at=audio_created_at,
            )

            self.messages.append(message)
            save_messages(self.chat_id, self.messages)

    def _save_recording(self):
        audio_path = get_audio_path(self.chat_id, get_new_audio_filename())
        self.ids.audio_recorder.save(audio_path)

        return os.path.basename(audio_path), os.path.getmtime(audio_path)


Builder.load_string(
    """
#:import AudioRecorderBox alkvin.uix.components.audio_recorder.AudioRecorderBox


<ChatScreen>:
    name: "chat"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: root.chat_id
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
            right_action_items: [["dots-vertical", lambda x: None]]
        
        ScrollView:
            MDBoxLayout:
                id: chat_box
                remove_message: lambda bubble_box: self.remove_widget(bubble_box)
                orientation: "vertical"
                adaptive_height: True
                padding: dp(40), dp(100), dp(40), dp(80)
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
            md_bg_color: [0.2, 0.6, 0.8, 1]

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
