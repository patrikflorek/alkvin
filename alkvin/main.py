import dotenv

dotenv.load_dotenv()

from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from alkvin.uix.home_screen import HomeScreen
from alkvin.uix.chat_screen import ChatScreen
from alkvin.uix.chats_screen import ChatsScreen
from alkvin.uix.robots_screen import RobotsScreen
from alkvin.uix.robot_screen import RobotScreen
from alkvin.uix.settings_screen import SettingsScreen

from alkvin.data import (
    get_new_chat_id,
    create_chat,
    get_default_robot_file,
    get_new_robot_file,
    create_robot,
)


def main():
    AlkvinApp().run()


class AlkvinApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return AppRoot()


class AppRoot(MDScreenManager):

    screens_history = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen())
        self.add_widget(ChatsScreen())
        self.add_widget(ChatScreen())
        self.add_widget(RobotsScreen())
        self.add_widget(RobotScreen())
        self.add_widget(SettingsScreen())

        Window.bind(on_keyboard=self._esc_to_previous_screen)

    def _esc_to_previous_screen(self, instance, key, *args):
        if key == 27:
            self.goto_previous_screen()
            return True
        return False

    def _goto_home_screen(self):
        self.current = "home"

    def _goto_chats_screen(self):
        self.current = "chats"

    def _goto_chat_screen(self, chat_id=None):
        if chat_id is None:
            chat_id = get_new_chat_id()
            create_chat(chat_id)

        self.get_screen("chat").chat_id = chat_id

        self.current = "chat"

    def _goto_robots_screen(self):
        self.current = "robots"

    def _goto_robot_screen(self, robot_file=None):
        if robot_file is None:
            robot_file = get_new_robot_file()
            create_robot(robot_file)

        self.get_screen("robot").robot_file = robot_file

        self.current = "robot"

    def _goto_settings_screen(self, **kwargs):
        self.current = "settings"

    def goto_previous_screen(self):
        self.screens_history.pop()  # pop the current screen

        if len(self.screens_history) > 0:
            screen_to_go_name_and_kwargs = self.screens_history.pop()
            if type(screen_to_go_name_and_kwargs) == str:
                screen_to_go_name = screen_to_go_name_and_kwargs
                kwargs = {}
            else:
                screen_to_go_name, kwargs = screen_to_go_name_and_kwargs

            self.goto_screen(screen_to_go_name, direction="back", **kwargs)

        elif self.current != "home":
            self.goto_screen("home", direction="back")

    def goto_screen(self, screen_name, direction="forward", **kwargs):
        self.transition.direction = "right" if direction == "back" else "left"

        screen_history_item = (screen_name, kwargs)
        if screen_history_item in self.screens_history:
            self.screens_history.remove(screen_history_item)

        self.screens_history.append((screen_name, kwargs))

        if screen_name == "home":
            self._goto_home_screen()
        elif screen_name == "chats":
            self._goto_chats_screen()
        elif screen_name == "chat":
            self._goto_chat_screen(chat_id=kwargs.get("chat_id"))
        elif screen_name == "robots":
            self._goto_robots_screen()
        elif screen_name == "robot":
            self._goto_robot_screen(robot_file=kwargs.get("robot_file"))
        elif screen_name == "settings":
            self._goto_settings_screen()
