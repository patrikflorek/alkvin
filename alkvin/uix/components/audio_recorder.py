import pyaudio

from kivy.clock import Clock
from kivy.properties import BooleanProperty

from kivymd.uix.boxlayout import MDBoxLayout

from kivy.lang import Builder

from alkvin.audio import AudioRecorder


# PyAudio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()


class AudioRecorderBox(MDBoxLayout):
    recording = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controls_timer = None
        self._recorder = AudioRecorder()

    def on_recording(self, instance, value):
        if value:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.ids.recording_timer.text = "00:00"

        self._recorder.open_stream()

        self._controls_timer = Clock.schedule_interval(self._update_controls, 0.5)

    def _update_controls(self, dt):
        if not self.recording:
            self._controls_timer.cancel()
            self._controls_timer = None
            return

        time = self._recorder.frame_count // RATE

        self.ids.recording_timer.text = f"{time // 60:02}:{time % 60:02}"

    def _stop_recording(self):
        self._recorder.close()

        self._controls_timer.cancel()
        self._controls_timer = None

        self.ids.recording_timer.text = "00:00"

    def save(self, file_path):
        self._recorder.save(file_path)


Builder.load_string(
    """
<AudioRecorderBox>:
    recording: False
    orientation: "horizontal"
    size_hint_y: None
    height: "96dp"
    padding: "24dp"
    md_bg_color: [1, .4, .2, .9]
    
    MDLabel:
        id: recording_timer
        text: "00:00"
        color: [1, 1, 1 , .9] if not root.recording else [0, 1, 0, .9]
        font_size: "24dp"
        halign: "right"
        padding: dp(24)
    """
)
