import os
import json

from functools import reduce

from datetime import datetime

from kivy.app import App

from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem

from alkvin.data import (
    load_chat,
    save_chat,
    delete_chat,
    load_messages,
    create_message,
    save_messages,
    get_audio_path,
    load_robot_list_items,
    load_robot,
)

from alkvin.uix.components.chat_bubble import ChatBubbleBox

from alkvin.audio import get_audio_bus

from alkvin.completion import generate_completion


class RobotsListItem(OneLineAvatarIconListItem):
    divider = None

    robot = DictProperty({"robot_name": ""})

    def __init__(self, robot, **kwargs):
        super().__init__(**kwargs)
        self.robot = robot
        self.app = App.get_running_app()

    def edit_robot(self):
        chat_screen = self.app.root.get_screen("chat")
        if chat_screen.select_robot_dialog is not None:
            chat_screen.select_robot_dialog.dismiss()
        self.app.root.goto_screen("robot", robot_file=self.robot["robot_file"])

    def on_release(self):
        self.ids.radio_check.active = True


class ChatScreen(MDScreen):
    chat_id = StringProperty()

    chat = DictProperty({"chat_title": "", "chat_summary": ""})

    robot = DictProperty({"robot_file": "", "robot_name": "", "robot_description": ""})

    messages = ListProperty()

    delete_chat_dialog = None

    select_robot_dialog = None

    selected_robot_file = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._audio_bus = get_audio_bus()
        self._audio_bus.set_on_save_recording_callback(self.on_save_recording)

    def on_enter(self, *args):
        prev_chat_id = self.chat.get("chat_id")

        self.chat = load_chat(self.chat_id)
        self.chat_id = self.chat["chat_id"]

        self.messages = load_messages(self.chat_id)

        robot_file = self.chat.get("chat_robot_file")

        # If the chat has a robot file and it is either the same as selected robot file or selected robot file is None, then load the robot
        if robot_file is not None and (
            robot_file == self.selected_robot_file or self.selected_robot_file is None
        ):
            self.robot = load_robot(robot_file)
            self.selected_robot_file = robot_file
        else:
            self.open_select_robot_dialog()

        # if not self.messages:
        #     self.create_completion_message()

        if self.chat_id != prev_chat_id:
            self.ids.chat_scroll.scroll_y = 1

    def on_pre_leave(self, *args):
        self._audio_bus.stop()

    def open_select_robot_dialog(self):
        robot_list_items = [
            RobotsListItem(robot_item_data)
            for robot_item_data in load_robot_list_items()
        ]

        for robot_list_item in robot_list_items:
            if robot_list_item.robot["robot_file"] == self.selected_robot_file:
                robot_list_item.ids.radio_check.active = True

        if self.selected_robot_file is None:
            self.selected_robot_file = robot_list_items[0].robot["robot_file"]
            robot_list_items[0].ids.radio_check.active = True

        if not self.select_robot_dialog:
            self.select_robot_dialog = MDDialog(
                title="Select a robot to chat with",
                type="confirmation",
                items=robot_list_items,
                buttons=[
                    MDFlatButton(
                        text="CREATE NEW",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda: self.manager.goto_screen("robot"),
                    ),
                    MDFlatButton(
                        text="SELECT",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.select_robot(
                            reduce(
                                lambda a, b: a if a.ids.radio_check.active else b,
                                robot_list_items,
                            )
                        ),
                    ),
                ],
                auto_dismiss=False,
            )
        else:
            print(self.select_robot_dialog, robot_list_items)
            self.select_robot_dialog.update_items(robot_list_items)

        self.select_robot_dialog.open()

    def select_robot(self, robot_item):
        self.selected_robot_file = robot_item.robot["robot_file"]
        self.robot = load_robot(robot_item.robot["robot_file"])
        self.chat["chat_robot_file"] = robot_item.robot["robot_file"]
        save_chat(self.chat)
        self.select_robot_dialog.dismiss()

    def on_messages(self, instance, messages):
        self.ids.chat_box.clear_widgets()
        for message in messages:
            self.ids.chat_box.add_widget(ChatBubbleBox(message))

    def on_save_recording(self, recording_path):
        audio_file = os.path.basename(recording_path)

        audio_created_at_timestamp = os.path.getmtime(recording_path)
        audio_created_at = datetime.fromtimestamp(
            audio_created_at_timestamp
        ).isoformat()

        message = create_message(
            self.chat_id,
            role="user",
            user_audio_file=audio_file,
            user_audio_created_at=audio_created_at,
        )

        self.messages.append(message)
        save_messages(self.chat_id, self.messages)

    def remove_message(self, index):
        self._delete_message_files(self.messages[index])

        del self.messages[index]
        save_messages(self.chat_id, self.messages)

    def change_message_index(self, message, index):
        current_index = self.messages.index(message)
        if current_index == index:
            return

        self.messages.remove(message)
        self.messages.insert(index, message)

        save_messages(self.chat_id, self.messages)

    def _delete_message_files(self, message):
        if message["role"] == "user":
            audio_path = get_audio_path(message["chat_id"], message["user_audio_file"])
            os.remove(audio_path)

    def save_messages(self):
        save_messages(self.chat_id, self.messages)

    def reload_messages(self):
        self.messages = load_messages(self.chat_id)

    def create_completion_message(self):
        generate_completion(
            self.robot["robot_instructions_prompt"],
            self.messages,
            self._on_completion_create_message,
        )

    def _on_completion_create_message(self, completion_text):
        self.messages.append(
            create_message(
                self.chat_id,
                role="assistant",
                completion_text=completion_text,
                completion_received_at=datetime.now().isoformat(),
            )
        )
        save_messages(self.chat_id, self.messages)
        self.reload_messages()

    def summarize_chat(self):
        summarization_massage = create_message(
            chat_id=self.chat_id,
            role="system",
            transcript_text=self.robot["robot_summarization_prompt"],
            message_sent_at=datetime.now().isoformat(),
        )
        summarization_messages = self.messages + [summarization_massage]

        generate_completion(
            self.robot["robot_instructions_prompt"],
            summarization_messages,
            self._on_summarized_chat,
        )

    def _on_summarized_chat(self, summary_str):
        summary = json.loads(summary_str)

        self.chat["chat_title"] = summary["title"]
        self.chat["chat_summary"] = summary["summary"]

        self.ids.chat_scroll.scroll_y = 1

        save_chat(self.chat)

    def open_delete_chat_dialog(self):
        if self.delete_chat_dialog is None:
            self.delete_chat_dialog = MDDialog(
                title="Delete chat",
                text="Are you sure you want to delete this chat?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.delete_chat_dialog.dismiss(),
                    ),
                    MDFlatButton(
                        text="DELETE",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self._delete_chat(),
                    ),
                ],
            )

        self.delete_chat_dialog.open()

    def _delete_chat(self):
        self.delete_chat_dialog.dismiss()
        delete_chat(self.chat_id)
        self.manager.goto_previous_screen()


Builder.load_string(
    """
#:import AudioRecorderBox alkvin.uix.components.audio_recorder.AudioRecorderBox


<ChatScreen>:
    name: "chat"
    
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: toolbar
            use_overflow: True
            title: root.chat['chat_title']
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
            right_action_items: 
                [
                ["file-document", lambda x: root.summarize_chat(), "Summarize chat", "Summarize chat"],
                ["robot", lambda x: root.open_select_robot_dialog(), "Select robot", "Select robot"],
                ["delete", lambda x: root.open_delete_chat_dialog(), "Delete chat", "Delete chat"],
                ]
        
        ScrollView:
            id: chat_scroll
            MDBoxLayout:
                orientation: "vertical"
                padding: "40dp"
                spacing: "40dp"
                adaptive_height: True

                MDCard:
                    orientation: "vertical"
                    padding: "24dp"
                    spacing: "12dp"
                    md_bg_color: [.4, .4, .4, .3]
                    radius: [25, 25, 25, 25]
                    elevation: 0
                    adaptive_height: True

                    MDLabel:
                        text: "Summary"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDSeparator:
                        height: "1dp"

                    MDLabel:
                        text: root.chat["chat_summary"]
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDIconButton:
                        icon: "chevron-down"
                        theme_text_color: "Custom"
                        text_color: [0.4, 0.4, 0.4, 0.8]
                        pos_hint: {"center_x": .5}
                        on_release: chat_scroll.scroll_y = 0

                MDBoxLayout:
                    id: chat_box
                    
                    remove_message: lambda bubble_box: root.remove_message(self.children[::-1].index(bubble_box))
                    save_messages: lambda: root.save_messages()
                    reload_messages: lambda: root.reload_messages()
                    create_completion_message: lambda: root.create_completion_message()

                    orientation: "vertical"
                    adaptive_height: True
                    # padding: dp(40)
                    spacing: dp(20)

        AudioRecorderBox:
            id: audio_recorder
            chat_id: root.chat_id


<RobotsListItem>:
    text: root.robot["robot_name"]

    IconLeftWidget:
        MDCheckbox:
            id: radio_check
            group: "robots"
            on_release: self.active = True

    IconRightWidget:
        icon: "pencil"
        disabled: not radio_check.active
        opacity: int(radio_check.active)
        on_release: root.edit_robot()
"""
)
