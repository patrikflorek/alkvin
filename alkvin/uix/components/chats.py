from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior


class ChatBubble(MDCard, RoundedRectangularElevationBehavior):
    chat_id = StringProperty()
    role = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Builder.load_string(
    """
<ChatBubble>:
    role: "assistant"
    text: ""
    audio_file: ""
    size_hint_y: None
    height: box.height
    md_bg_color: [1, .4, .2, .2] if self.role == "user" else [.5, .5, 1, .6]
    radius: [25, 25, 25, 0] if self.role == "user" else [25, 0, 25, 25]

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
