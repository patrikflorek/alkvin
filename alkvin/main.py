from kivy.core.window import Window

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

    previous_screen_name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen())
        self.add_widget(ChatScreen())
        self.add_widget(SettingsScreen())

        Window.bind(on_keyboard=self._goto_previous_screen)

    def _goto_previous_screen(self, instance, key, *args):
        if key == 27:
            self.goto_previous_screen()
            return True
        return False

    def goto_previous_screen(self):
        if self.previous_screen_name:
            self.goto_screen(self.previous_screen_name, direction="back")
        elif self.current != "home":
            self.goto_screen("home", direction="back")

    def goto_screen(self, screen_name, direction="forward"):
        if direction == "back":
            self.previous_screen_name = ""
            self.transition.direction = "right"
        else:
            self.previous_screen_name = self.current
            self.transition.direction = "left"

        self.current = screen_name
