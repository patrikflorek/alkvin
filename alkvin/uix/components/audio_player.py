from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar

from alkvin.audio import get_audio_player


class AudioPlayerBox(MDBoxLayout):
    audio_path = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controls_timer = None
        self._player = get_audio_player()

    def start_playing(self):
        self.ids.playing_progress.value = 0.1

        self._player.play(self, self.audio_path)

        self._controls_timer = Clock.schedule_interval(self._update_controls, 0.1)

    def _update_controls(self, dt):
        if not self._player.is_streaming_widget(self) or self._player.progress == 1.0:
            if self._controls_timer is not None:
                self._controls_timer.cancel()
                self._controls_timer = None

            Clock.schedule_once(self._reset_controls, 0.1)

        self.ids.playing_progress.value = self._player.progress * 100

    def _reset_controls(self, dt):
        self.ids.playing_progress.value = 0.1


class PlayingProgressBar(MDProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0.1
        self.max = 100
        self.value = 0.1


Builder.load_string(
    """
# <PlayingProgressBar>:


<AudioPlayerBox>:
    progress_bar_color: .4, .4, .4, .8
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
        on_release: root.start_playing()
    
    MDBoxLayout:
        padding: dp(10), dp(20), dp(30), dp(20)
        PlayingProgressBar:
            id: playing_progress
            color: root.progress_bar_color
            
"""
)
