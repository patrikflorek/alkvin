import os

from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from alkvin.data import (
    create_robot,
    load_robot,
    save_robot,
    delete_robot,
    robot_file_exists,
)


class ReplicatedRobotScreen(MDScreen):
    robot_file = StringProperty()

    robot = DictProperty(
        {
            "robot_file": "",
            "robot_name": "",
            "robot_description": "",
            "robot_language": "",
            "robot_speech_to_text_model": "",
            "robot_speech_to_text_prompt": "",
            "robot_text_generation_model": "",
            "robot_instructions_prompt": "",
            "robot_summarization_prompt": "",
            "robot_text_to_speech_model": "",
        }
    )

    delete_robot_dialog = None

    def create_robot_replica(self, robot_file):
        orig_robot = load_robot(robot_file)
        self.robot = orig_robot.copy()

        orig_file_name, file_extension = os.path.splitext(robot_file)
        replica_file_name = orig_file_name + "_replica"
        replica_count = 1

        while robot_file_exists(
            f"{replica_file_name}_{replica_count}" + file_extension
        ):
            replica_count += 1

        self.robot["robot_file"] = (
            f"{replica_file_name}_{replica_count}" + file_extension
        )
        self.robot["robot_name"] = "Replica of " + self.robot["robot_name"]

        create_robot(self.robot["robot_file"])

        save_robot(self.robot)

        self.robot_file = self.robot["robot_file"]

    def on_pre_enter(self, *args):
        prev_robot_file = self.robot.get("robot_file")

        self.robot = load_robot(self.robot_file)

        if self.robot_file != prev_robot_file:
            self.ids.robot_scroll.scroll_y = 1

    def on_pre_leave(self, *args):
        if not robot_file_exists(self.robot_file):
            return

        if self.robot_file != self.robot["robot_file"]:
            delete_robot(self.robot_file)
            # self.robot_file = self.robot["robot_file"]

        save_robot(self.robot)

    def open_delete_robot_dialog(self):
        if self.delete_robot_dialog is None:
            self.delete_robot_dialog = MDDialog(
                title="Delete robot",
                text="Are you sure you want to delete this robot?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.delete_robot_dialog.dismiss(),
                    ),
                    MDFlatButton(
                        text="DELETE",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self._delete_robot(),
                    ),
                ],
            )

        self.delete_robot_dialog.open()

    def _delete_robot(self):
        self.delete_robot_dialog.dismiss()
        delete_robot(self.robot_file)
        self.manager.goto_previous_screen()


Builder.load_string(
    """
#:import os os


<ReplicatedRobotScreen>:
    name: "replicated_robot"
    
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: toolbar
            use_overflow: True
            title: root.robot['robot_name']
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
            right_action_items: 
                [["delete", lambda x: root.open_delete_robot_dialog(), "Delete robot", "Delete robot"]]       
        ScrollView:
            id: robot_scroll
            MDBoxLayout:
                orientation: "vertical"
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True

                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: robot_file.height

                    MDTextField:
                        id: robot_file
                        hint_text: "Robot file name"
                        helper_text: "Enter the name of the robot file"
                        helper_text_mode: "on_focus"
                        required: True
                        text: root.robot["robot_file"].split(".")[0]
                        on_text: root.robot["robot_file"] = self.text + ".json"

                    MDLabel:
                        text: ".json"
                        halign: "center"
                        valign: "middle"
                        size_hint_x: None
                        width: "64dp"

                MDTextField:
                    id: robot_name
                    hint_text: "Robot name"
                    helper_text: "Enter the name of the robot"
                    helper_text_mode: "on_focus"
                    required: True
                    text: root.robot['robot_name']
                    on_text: root.robot['robot_name'] = self.text

                MDTextField:
                    id: robot_description
                    hint_text: "Robot description"
                    helper_text: "Enter a description of the robot"
                    helper_text_mode: "on_focus"
                    required: True
                    text: root.robot['robot_description']
                    on_text: root.robot['robot_description'] = self.text

                MDTextField:
                    id: robot_language
                    hint_text: "Robot language"
                    helper_text: "Enter the language of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_language']
                    on_text: root.robot['robot_language'] = self.text

                MDTextField:
                    id: robot_speech_to_text_model
                    hint_text: "Speech-to-text model"
                    helper_text: "Enter the speech-to-text model of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_speech_to_text_model']
                    on_text: root.robot['robot_speech_to_text_model'] = self.text

                MDTextField:
                    id: robot_speech_to_text_prompt
                    hint_text: "Speech-to-text prompt"
                    helper_text: "Enter the speech-to-text prompt of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_speech_to_text_prompt']
                    on_text: root.robot['robot_speech_to_text_prompt'] = self.text

                MDTextField:
                    id: robot_text_generation_model
                    hint_text: "Text generation model"
                    helper_text: "Enter the text generation model of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_text_generation_model']
                    on_text: root.robot['robot_text_generation_model'] = self.text

                MDTextField:
                    id: robot_instructions_prompt
                    hint_text: "Instructions prompt"
                    helper_text: "Enter the instructions prompt of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_instructions_prompt']
                    on_text: root.robot['robot_instructions_prompt'] = self.text

                MDTextField:
                    id: robot_summarization_prompt
                    hint_text: "Summarization prompt"
                    helper_text: "Enter the summarization prompt of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_summarization_prompt']
                    on_text: root.robot['robot_summarization_prompt'] = self.text

                MDTextField:
                    id: robot_text_to_speech_model
                    hint_text: "Text-to-speech model"
                    helper_text: "Enter the text-to-speech model of the robot"
                    helper_text_mode: "on_focus"
                    required: False
                    text: root.robot['robot_text_to_speech_model']
                    on_text: root.robot['robot_text_to_speech_model'] = self.text
"""
)
