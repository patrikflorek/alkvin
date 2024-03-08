from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout

from alkvin.audio import get_audio_bus


class AudioPlayerBox(MDBoxLayout):
    state = StringProperty("stop")
    audio_path = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controls_timer = None
        self._audio_bus = get_audio_bus()

    def on_state(self, instance, state):
        if state == "stop":
            if self._controls_timer is not None:
                self._controls_timer.cancel()
                self._controls_timer = None

                self.ids.playing_progress.value = 0.1

        elif state == "play":
            self._controls_timer = Clock.schedule_interval(self._update_controls, 0.1)

    def _update_controls(self, dt):
        self.ids.playing_progress.value = (
            (self._audio_bus.passed_time / self._audio_bus.total_time * 100)
            if self._audio_bus.total_time
            else 0.1
        )

    def toggle_playing(self):
        if self.state == "stop":
            self._audio_bus.play(self, self.audio_path)

        elif self.state == "play":
            self._audio_bus.stop(self)


Builder.load_string(
    """
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
        icon: "play" if root.state == "stop" else "stop"
        theme_text_color: "Custom"
        text_color: [.4, .4, .4]
        on_release: root.toggle_playing()
    
    MDBoxLayout:
        padding: dp(10), dp(20), dp(30), dp(20)
        MDProgressBar:
            id: playing_progress
            min: 0.1
            max: 100
            value: 0.1
            color: root.progress_bar_color
            
"""
)
