from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

from kivymd.uix.screen import MDScreen


class HomeScreen(MDScreen):
    pass


Builder.load_string(
    """
<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Alkvin"

        ScrollView:
            MDGridLayout:
                id: grid
                cols: 1 if self.width < 520 else 2
                padding: dp(40), dp(80)
                spacing: dp(40)
                size_hint_y: None
                height: self.minimum_height

                AnchorLayout:
                    anchor_x: "center" if grid.cols == 1 else "right"
                    anchor_y: "center"
                    size_hint_y: None
                    height: dp(200)
                    
                    MDCard:
                        id: chats_card
                        orientation: "vertical"
                        size_hint: None, None
                        size: dp(200), dp(200)
                        padding: dp(40)
                        spacing: dp(20)
                        radius: [20, 20, 20, 20]
                        md_bg_color: app.theme_cls.primary_color
                        on_release: app.root.goto_screen("chats")

                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                        
                            MDIcon:
                                icon: "forum"
                                font_size: "80sp"
                                color: "white"

                        MDLabel:
                            text: "Chats"
                            halign: "center"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "white"
                            size_hint_y: None
                            height: dp(48)

                AnchorLayout:
                    anchor_x: "center" if grid.cols == 1 else "left"
                    anchor_y: "center"
                    size_hint_y: None
                    height: dp(200)
                    
                    MDCard:
                        id: users_card
                        orientation: "vertical"
                        size_hint: None, None
                        size: dp(200), dp(200)
                        padding: dp(40)
                        spacing: dp(20)
                        radius: [20, 20, 20, 20]
                        md_bg_color: app.theme_cls.primary_color
                        on_release: print("Users")

                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                        
                            MDIcon:
                                icon: "account-voice"
                                font_size: "80sp"
                                color: "white"

                        MDLabel:
                            text: "Users"
                            halign: "center"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "white"
                            size_hint_y: None
                            height: dp(48)

                AnchorLayout:
                    anchor_x: "center" if grid.cols == 1 else "right"
                    anchor_y: "center"
                    size_hint_y: None
                    height: dp(200)
                    
                    MDCard:
                        id: assistants_card
                        orientation: "vertical"
                        size_hint: None, None
                        size: dp(200), dp(200)
                        padding: dp(40)
                        spacing: dp(20)
                        radius: [20, 20, 20, 20]
                        md_bg_color: app.theme_cls.primary_color
                        on_release: print("Assistants")

                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                        
                            MDIcon:
                                icon: "robot"
                                font_size: "80sp"
                                color: "white"

                        MDLabel:
                            text: "Assistants"
                            halign: "center"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "white"
                            size_hint_y: None
                            height: dp(48)

                AnchorLayout:
                    anchor_x: "center" if grid.cols == 1 else "left"
                    anchor_y: "center"
                    size_hint_y: None
                    height: dp(200)
                    
                    MDCard:
                        id: settings_card
                        orientation: "vertical"
                        size_hint: None, None
                        size: dp(200), dp(200)
                        padding: dp(40)
                        spacing: dp(20)
                        radius: [20, 20, 20, 20]
                        md_bg_color: app.theme_cls.primary_color
                        on_release: print("Settings")

                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                        
                            MDIcon:
                                icon: "cogs"
                                font_size: "80sp"
                                color: "white"

                        MDLabel:
                            text: "Settings"
                            halign: "center"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: "white"
                            size_hint_y: None
                            height: dp(48)
"""
)
