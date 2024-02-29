from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout

from alkvin.audio import get_audio_player


class AudioPlayerBox(MDBoxLayout):
    audio_path = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controls_timer = None
        self._player = get_audio_player()


Builder.load_string(
    """
<AudioPlayerBox>:
    audio_path: ""
    orientation: "horizontal"
    size_hint_y: None
    height: "48dp"
    canvas:
        Color:
            rgba: 1, 1, 1, .6
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [24, 24, 24, 24]
    
    MDIconButton:
        icon: "play"
        theme_text_color: "Custom"
        text_color: [.4, .4, .4]
        on_release: root._player.play(root.audio_path)
    
    MDBoxLayout:
        padding: dp(10), dp(20), dp(30), dp(20)
        MDProgressBar:
            id: playing_progress
            value: 0
"""
)
