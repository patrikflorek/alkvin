from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen


from alkvin.data import load_chat_list_items


class ChatsScreen(MDScreen):
    chat_list_items = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.chat_list_items = load_chat_list_items()


class ChatListItem(TwoLineListItem):
    chat_id = StringProperty()
    chat_title = StringProperty()
    chat_summary = StringProperty()


Builder.load_string(
    """
<ChatsScreen>:
    name: "chats"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Chats"
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
        
        RecycleView:
            data: root.chat_list_items
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
            icon: "message-plus"
            type: "large"
            elevation_normal: 12
            on_release: app.root.goto_screen("chat")


<ChatListItem>:
    text: self.chat_title
    secondary_text: self.chat_summary
    on_release: app.root.goto_screen("chat", chat_id=self.chat_id)
"""
)
