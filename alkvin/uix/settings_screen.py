from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)


Builder.load_string(
    """
<SettingsScreen>:
    name: "settings"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Settings"
            left_action_items: [["arrow-left", lambda x: app.root.goto_previous_screen()]]
        MDBoxLayout:
            MDLabel:
                text: "SETTINGS SCREEN"
                halign: "center"
                pos_hint: {"center_x": 0.5, "center_y": 0.75}
"""
)
