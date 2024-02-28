from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.uix.card import MDCard


class ChatBubble(RecycleDataViewBehavior, MDCard):
    chat_id = StringProperty()
    role = StringProperty()
    user_audio_file = StringProperty()
    user_audio_created_at = StringProperty()
    message_sent_at = StringProperty()
    transcript_text = StringProperty()
    transcript_received_at = StringProperty()
    transcript_price = StringProperty()
    completion_text = StringProperty()
    completion_received_at = StringProperty()
    completion_price = StringProperty()
    tts_audio_file = StringProperty()
    tts_audio_received_at = StringProperty()
    tts_audio_price = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        print("refresh_view_attrs", index, data)

        if data["role"] == "user":
            self._show_user_message_box()
            print("role: user")

            self.radius = [25, 25, 25, 0]

            if data["message_sent_at"]:
                self._hide_prepared_message_control_box()
                self.md_bg_color = [1, 0.4, 0.2, 0.6]
            else:
                self._show_prepared_message_control_box()
                self.md_bg_color = [1, 0.4, 0.2, 0.3]

        elif data["role"] == "assistant":
            self._show_assistant_message_box()
            print("role: assistant")

            self.radius = [25, 0, 25, 25]
            self.md_bg_color = [0.2, 0.6, 0.8, 0.6]

        print()
        return super().refresh_view_attrs(rv, index, data)

    def _show_user_message_box(self):
        self.ids.user_message_box.disabled = False
        self.ids.user_message_box.height = (
            self.ids.user_message_content_box.height + dp(48)
        )
        self.ids.user_message_box.opacity = 1

        self.ids.assistant_message_box.disabled = True
        self.ids.assistant_message_box.height = 0
        self.ids.assistant_message_box.opacity = 0

    def _show_assistant_message_box(self):
        self.ids.user_message_box.disabled = True
        self.ids.user_message_box.height = 0
        self.ids.user_message_box.opacity = 0

        self.ids.assistant_message_box.disabled = False
        self.ids.assistant_message_box.height = (
            self.ids.completion_box.height + self.ids.tts_audio_box.height + dp(60)
        )
        self.ids.assistant_message_box.opacity = 1

    def _show_prepared_message_control_box(self):
        self.ids.prepared_message_control_box.disabled = False
        self.ids.prepared_message_control_box.width = "48dp"
        self.ids.prepared_message_control_box.opacity = 1

    def _hide_prepared_message_control_box(self):
        self.ids.prepared_message_control_box.disabled = True
        self.ids.prepared_message_control_box.width = 0
        self.ids.prepared_message_control_box.opacity = 0


Builder.load_string(
    """
<AudioPlayerBox@MDBoxLayout>:
    orientation: "horizontal"
    size_hint_y: None
    height: "48dp"
    canvas:
        Color:
            rgba: 1, 1, 1, .6
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [24, 24, 24, 24]
    
    MDIconButton:
        icon: "play"
        user_font_size: "24dp"
        on_release: print("Play audio")
    
    MDBoxLayout:
        padding: dp(10), dp(20), dp(30), dp(20)
        MDProgressBar:
            value: 0


<ChatBubble>:
    orientation: "vertical"
    adaptive_height: True
    md_bg_color: [.4, .4, .4, .6]

    radius: [25, 25, 25, 25]
    MDBoxLayout:
        id: user_message_box
        orientation: "horizontal"
        padding: "24dp"
        spacing: "12dp"
        size_hint_y: None
        height: user_message_content_box.height + dp(48)

        MDBoxLayout:
            id: user_message_content_box
            orientation: "vertical"
            adaptive_height: True
            spacing: "8dp"
            
            AudioPlayerBox:
                id: user_audio_box               
            MDBoxLayout:
                id: transcript_box
                orientation: "vertical"
                adaptive_height: True
                MDIconButton:
                    icon: "typewriter"
                    user_font_size: "24dp"
                    theme_text_color: "Custom"
                    text_color: [.4, .4, .4]
                    on_release: print("Transcribe audio")

        MDRelativeLayout:
            id: prepared_message_control_box
            size_hint_x: None
            width: "48dp"
            AnchorLayout:
                anchor_x: "right"
                anchor_y: "top"
                MDIconButton:
                    icon: "close"
                    user_font_size: "18dp"
                    theme_text_color: "Custom"
                    text_color: [.4, .4, .4]
                    on_release: print("Close")
            AnchorLayout:
                anchor_x: "right"
                anchor_y: "bottom"
                MDIconButton:
                    icon: "send"
                    user_font_size: "64dp"
                    theme_text_color: "Custom"
                    text_color: [.4, .4, .4]
                    on_release: print("Send")

    MDBoxLayout:
        id: assistant_message_box
        orientation: "vertical"
        padding: "24dp"
        spacing: "12dp"
        size_hint_y: None
        height: completion_box.height + tts_audio_box.height + dp(60)

        MDBoxLayout:
            id: completion_box
        
        AudioPlayerBox:
            id: tts_audio_box

"""
)
