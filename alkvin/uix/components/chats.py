from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior


class ChatListItem(OneLineListItem):
    chat_id = StringProperty()

    def __init__(self, chat_id="", **kwargs):
        super().__init__(**kwargs)


class ChatBubble(MDCard, RoundedRectangularElevationBehavior):
    chat_id = StringProperty()
    role = StringProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Builder.load_string(
    """
<ChatListItem>:
    chat_id: ""
    text: self.chat_id
    on_release: app.root.goto_screen("chat", chat_id=self.chat_id)


<ChatBubble>:
    role: "assistant"
    text: ""
    audio_file: ""
    size_hint_y: None
    height: box.height
    md_bg_color: [1, .4, .2, .6] if self.role == "user" else [.5, .5, 1, .6]
    radius: [25, 25, 25, 0] if self.role == "user" else [25, 0, 25, 25]

    MDBoxLayout:
        id: box
        orientation: "vertical"
        padding: "24dp"
        spacing: "12dp"
        size_hint_y: None
        height: label.height + audio_box.height + dp(60)

        MDLabel:
            id: label
            text: root.text
            text_size: self.width, None
            halign: "left"
            size_hint_y: None
            height: self.texture_size[1]
            color: .2, .2, .2, .8
        
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


"""
)
