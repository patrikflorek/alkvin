from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen


from alkvin.data import load_robot_list_items


class RobotsScreen(MDScreen):
    robot_list_items = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.robot_list_items = load_robot_list_items()


class RobotListItem(TwoLineListItem):
    robot_file = StringProperty()
    robot_name = StringProperty()
    robot_description = StringProperty()


Builder.load_string(
    """
<RobotsScreen>:
    name: "robots"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Robots"
            left_action_items: [["home", lambda x: app.root.goto_screen("home")]]
        
        RecycleView:
            data: root.robot_list_items
            viewclass: "RobotListItem"

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
            icon: "robot-love"
            type: "large"
            elevation_normal: 12
            on_release: app.root.goto_screen("robot")


<RobotListItem>:
    text: self.robot_name
    secondary_text: self.robot_description
    on_release: app.root.goto_screen("robot", robot_file=self.robot_file)
"""
)
