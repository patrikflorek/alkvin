from kivy.clock import Clock
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.lang import Builder

from alkvin.audio import get_audio_bus

from alkvin.data import get_new_audio_filename, get_audio_path


class AudioRecorderBox(MDRelativeLayout):
    chat_id = StringProperty()
    state = StringProperty("stop")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controls_timer = None
        self._audio_bus = get_audio_bus()

    def on_state(self, instance, state):
        if state == "stop":
            if self._controls_timer is not None:
                self._controls_timer.cancel()
                self._controls_timer = None

                self.ids.recording_timer.text = "00:00:00"

        elif state == "record":
            self._controls_timer = Clock.schedule_interval(self._update_controls, 0.1)

    def _update_controls(self, dt):
        if self._audio_bus.passed_time is None:
            return

        time_min_sec_hun = int(self._audio_bus.passed_time * 100)

        time_hun = time_min_sec_hun % 100
        time_min_sec = time_min_sec_hun // 100
        time_min = time_min_sec // 60
        time_sec = time_min_sec % 60
        self.ids.recording_timer.text = f"{time_min:02}:{time_sec:02}:{time_hun:02}"

    def toggle_recording(self):
        if self.state == "stop":
            new_audio_filename = get_new_audio_filename()
            new_audio_path = get_audio_path(self.chat_id, new_audio_filename)
            self._audio_bus.record(self, new_audio_path)

        elif self.state == "record":
            self._audio_bus.stop(self)


Builder.load_string(
    """
<AudioRecorderBox>:
    recording: False
    size_hint_y: None
    height: "96dp"
    md_bg_color: [1, .4, .2, .9]

    AnchorLayout:
        anchor_x: "left"
        anchor_y: "center"
        padding: "48dp", 0, 0, "96dp"        
        MDFloatingActionButton:
            icon: "microphone"
            text_color: [0, 1, 0] if root.state == "record" else [1, 1, 1]
            type: "large"
            elevation_normal: 12
            on_release: root.toggle_recording()
            md_bg_color: [1, .4, .2, 1]
    
    AnchorLayout:
        anchor_x: "right"
        anchor_y: "center"
        padding: 0, 0, "24dp", 0
        MDLabel:
            id: recording_timer
            text: "00:00:00"
            color: [0, 1, 0 , .9] if root.state == "record" else [1, 1, 1, .9]
            font_size: "24dp"
            halign: "right"
            padding: dp(24)
    """
)
