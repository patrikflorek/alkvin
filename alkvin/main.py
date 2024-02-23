from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from alkvin.uix.home_screen import HomeScreen
from alkvin.uix.chat_screen import ChatScreen
from alkvin.uix.settings_screen import SettingsScreen


def main():
    AlkvinApp().run()


class AlkvinApp(MDApp):
    def build(self):
        return AppRoot()


class AppRoot(MDScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen(name="home"))
        self.add_widget(ChatScreen(name="chat"))
        self.add_widget(SettingsScreen(name="settings"))
