from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

from alkvin.data import get_audio_path

from alkvin.transcription import transcribe_audio


class ChatBubbleBox(MDBoxLayout):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.chat_id = message["chat_id"]
        self.role = message["role"]

        if self.role == "user":
            if not message["message_sent_at"]:
                self.bubble = UserPreparedMessageChatBubble(message)
            else:
                self.bubble = UserSentMessageChatBubble(message)

        elif self.role == "assistant":
            self.bubble = AssistantReceivedMessageChatBubble(message)

        else:
            self.bubble = BaseChatBubble(message)

        self.add_widget(self.bubble)

    def close(self):
        self.parent.remove_message(self)


class BaseChatBubble(MDCard):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.chat_id = message["chat_id"]
        self.role = message["role"]


class UserPreparedMessageChatBubble(BaseChatBubble):
    transcript_text = StringProperty()
    user_audio_path = StringProperty()

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.message = message
        self.user_audio_file = message["user_audio_file"]
        self.user_audio_path = get_audio_path(self.chat_id, self.user_audio_file)

        self.user_audio_created_at = message["user_audio_created_at"]
        self.transcript_text = message.get("transcript_text", "")
        self.transcript_received_at = message.get("transcript_received_at", "")

        if self.transcript_text:
            self._show_transcript_label()
        else:
            self._show_transcript_button()

    def _show_transcript_button(self):
        self.ids.transcript_button_box.disabled = False
        self.ids.transcript_button_box.height = "48dp"
        self.ids.transcript_button.opacity = 1

        self.ids.transcript_label.disabled = True
        self.ids.transcript_label.height = 0
        self.ids.transcript_label.opacity = 0

    def _show_transcript_label(self):
        self.ids.transcript_label.disabled = False
        self.ids.transcript_label.height = "48dp"
        self.ids.transcript_label.opacity = 1

        self.ids.transcript_button_box.disabled = True
        self.ids.transcript_button_box.height = 0
        self.ids.transcript_button.opacity = 0

    def transcribe_audio(self):
        transcribe_audio(self.user_audio_path, self._on_transcription_callback)

    def _on_transcription_callback(self, text):
        self.transcript_text = text

    def on_transcript_text(self, instance, value):
        self.message["transcript_text"] = value
        self._show_transcript_label()

    def close(self):
        if self.ids.user_audio_player.state == "play":
            self.ids.user_audio_player.stop()

        self.parent.remove_message(self)


class UserSentMessageChatBubble(BaseChatBubble):
    transcript_text = StringProperty()
    user_audio_path = StringProperty()

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.user_audio_file = message["user_audio_file"]
        self.user_audio_path = get_audio_path(self.chat_id, self.user_audio_file)

        self.transcript_text = message["transcript_text"]
        self.transcript_received_at = message["transcript_received_at"]
        self.message_sent_at = message["message_sent_at"]


class AssistantReceivedMessageChatBubble(BaseChatBubble):
    completion_text = StringProperty()
    tts_audio_path = StringProperty()

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.completion_text = message["completion_text"]
        self.completion_received_at = message["completion_received_at"]

        self.tts_audio_file = message.get("tts_audio_file", "")
        self.tts_audio_path = get_audio_path(self.chat_id, self.tts_audio_file)

        self.tts_audio_received_at = message.get("tts_audio_received_at", "")

        if self.tts_audio_file:
            self.ids.synthesize_button_box.disabled = True
            self.ids.synthesize_button_box.height = 0
            self.ids.synthesize_button.opacity = 0
        else:
            self.ids.tts_audio_player.disabled = True
            self.ids.tts_audio_player.height = 0
            self.ids.tts_audio_player.opacity = 0


Builder.load_string(
    """
#:import AudioPlayerBox alkvin.uix.components.audio_player.AudioPlayerBox 

<ChatBubbleBox>:
    adaptive_height: True


<BaseChatBubble>:
    padding: "24dp"
    spacing: "12dp"
    md_bg_color: [.4, .4, .4, .6]
    radius: [25, 25, 25, 25]
    adaptive_height: True

    
<UserPreparedMessageChatBubble>:
    md_bg_color: [1, .4, .2, .3]
    radius: [25, 25, 25, 0]

    MDBoxLayout:
        id: content_box
        orientation: "vertical"
        adaptive_height: True
        spacing: "24dp"

        AudioPlayerBox:
            id: user_audio_player
            audio_path: root.user_audio_path
            progress_bar_color: [1, .4, .2, .8]

        MDBoxLayout:
            id: transcript_box
            orientation: "vertical"
            adaptive_height: True

            MDBoxLayout:
                id: transcript_button_box
                size_hint_y: None
                height: transcript_button.height

                MDIconButton:
                    id: transcript_button
                    icon: "typewriter"
                    theme_text_color: "Custom"
                    text_color: [.4, .4, .4]
                    size_hint_y: None
                    height: "48dp"
                    on_release: root.transcribe_audio()

            MDLabel:
                id: transcript_label
                text: root.transcript_text
                theme_text_color: "Custom"
                text_color: [.4, .4, .4]
                font_style: "Body2"
                adaptive_height: True
        
    MDRelativeLayout:
        id: control_box
        size_hint_x: None
        width: "48dp"

        AnchorLayout:
            anchor_x: "right"
            anchor_y: "top"
            MDIconButton:
                icon: "close"
                icon_size: "18dp"
                theme_text_color: "Custom"
                text_color: [.4, .4, .4]
                on_release: root.parent.close()

        AnchorLayout:
            anchor_x: "right"
            anchor_y: "bottom"
            MDIconButton:
                icon: "send"
                icon_size: "24dp"
                theme_text_color: "Custom"
                text_color: [.4, .4, .4]
                on_release: print("Send")  


<UserSentMessageChatBubble>:
    orientation: "vertical"
    md_bg_color: [1, .4, .2, .6]
    radius: [25, 25, 25, 0]
    spacing: "24dp"

    AudioPlayerBox:
        id: user_audio_player
        audio_path: root.user_audio_path
        progress_bar_color: [1, .4, .2, .8]

    MDLabel:
        id: transcript_label
        text: root.transcript_text
        theme_text_color: "Custom"
        text_color: [.4, .4, .4]
        font_style: "Body2"
        adaptive_height: True


<AssistantReceivedMessageChatBubble>:
    orientation: "vertical"
    md_bg_color: [.2, .6, .8, .6]
    radius: [25, 0, 25, 25]

    MDLabel:
        id: completion_label
        text: root.completion_text
        theme_text_color: "Custom"
        text_color: [.4, .4, .4]
        font_style: "Body1"
        adaptive_height: True


    MDBoxLayout:
        id: speech_synthesize_box
        orientation: "vertical"
        adaptive_height: True

        MDBoxLayout: 
            id: synthesize_button_box
            size_hint_y: None
            height: synthesize_button.height

            MDIconButton:
                id: synthesize_button
                icon: "account-voice"
                theme_text_color: "Custom"
                text_color: [.4, .4, .4]
                on_release: print("Synthesize speech")

        AudioPlayerBox:
            id: tts_audio_player
            audio_path: root.tts_audio_path
            progress_bar_color: [.2, .6, .8, .8]        
"""
)
