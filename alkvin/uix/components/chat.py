from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class ChatBubble(RecycleDataViewBehavior, MDCard):
    chat_id = StringProperty()
    role = StringProperty()
    audio_file = StringProperty()
    audio_created_at = StringProperty()
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


Builder.load_string(
    """
<ChatBubble>:
    size_hint_y: None
    md_bg_color: [.2, .6, .8, .6]
    adaptive_height: True
    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        padding: "8dp"
        spacing: "8dp"
        MDLabel:
            text: root.chat_id
            size_hint_y: None
            height: self.texture_size[1]

<OldChatBubble>:
    role: "assistant"
    audio_file: ""
    size_hint_y: None
    height: box.height
    md_bg_color: [.4, .4, .4, .3]
    radius: [25, 25, 25, 25]

    MDBoxLayout:
        id: box
        orientation: "horizontal"
        padding: "24dp"
        spacing: "12dp"
        size_hint_y: None
        height: self.minimum_height

        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            spacing: "8dp"

            MDBoxLayout:
                id: audio_box
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
                        value: 50
                        # size_hint_x: None
                        # width: root.width - dp(48)
            
            MDIconButton:
                icon: "typewriter"
                user_font_size: "24dp"
                theme_text_color: "Custom"
                text_color: [.4, .4, .4]
                on_release: print("Transcribe audio")

            # MDLabel:
            #     id: label
            #     text: root.text
            #     text_size: self.width, None
            #     halign: "left"
            #     size_hint_y: None
            #     height: self.texture_size[1]
            #     color: .2, .2, .2, .8
        MDRelativeLayout:
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
            # padding: 0, 0, dp(24), dp(24)
            # size_hint: None, None
            # size: "48dp", "48dp"
            # MDFloatingActionButton:
            #     icon: "dots-vertical"
            #     elevation_normal: 0
            #     size_hint: None, None
            #     size: "48dp", "48dp"
            #     md_bg_color: 1, 1, 1, 0
            #     on_release: print("More options")
"""
)
