from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(
            MDLabel(
                text="HOME SCREEN",
                halign="center",
                pos_hint={"center_x": 0.5, "center_y": 0.75},
            )
        )
        self.add_widget(
            MDRectangleFlatButton(
                text="CHAT SCREEN",
                pos_hint={"center_x": 0.25, "center_y": 0.5},
            )
        )
        self.add_widget(
            MDRectangleFlatButton(
                text="SETTINGS SCREEN",
                pos_hint={"center_x": 0.75, "center_y": 0.5},
            )
        )
