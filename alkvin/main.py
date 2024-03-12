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

    previous_screen_name = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(HomeScreen())
        self.add_widget(ChatsScreen())
        self.add_widget(ChatScreen())
        self.add_widget(RobotsScreen())
        self.add_widget(RobotScreen())
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

    def goto_screen(self, screen_name, direction="forward", **kwargs):
        if direction == "back":
            self.previous_screen_name = ""
            self.transition.direction = "right"
        else:
            if screen_name == "chat":
                chat_id = kwargs.get("chat_id")
                if chat_id is None:
                    chat_id = get_new_chat_id()
                    create_chat(chat_id)

                robot_file = kwargs.get("robot_file")
                if robot_file is None:
                    robot_file = get_default_robot_file()
                    create_robot(robot_file)

                self.get_screen("chat").chat_id = chat_id
                self.get_screen("chat").robot_file = robot_file

            if screen_name == "robot":
                robot_file = kwargs.get("robot_file")
                if robot_file is None:
                    robot_file = get_new_robot_file()
                    create_robot(robot_file)

                self.get_screen(screen_name).robot_file = robot_file

            self.previous_screen_name = self.current
            self.transition.direction = "left"

        self.current = screen_name
