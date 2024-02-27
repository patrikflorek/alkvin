from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen


from alkvin.data import load_chat_ids


class HomeScreen(MDScreen):
    chat_ids = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.chat_ids = load_chat_ids()


class ChatListItem(OneLineListItem):
    chat_id = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Builder.load_string(
    """
<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Chats"
            right_action_items: [["cog", lambda x: app.root.goto_screen("settings")]]
        
        RecycleView:
            data: root.chat_ids
            viewclass: "ChatListItem"

            RecycleBoxLayout:
                orientation: "vertical"
                default_size: None, None
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
    
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "bottom"
        padding: dp(48)        
        MDFloatingActionButton:
            icon: "chat"
            type: "large"
            elevation_normal: 12
            on_release: app.root.goto_screen("chat")


<ChatListItem>:
    chat_id: ""
    text: self.chat_id
    on_release: app.root.goto_screen("chat", chat_id=self.chat_id)
"""
)
