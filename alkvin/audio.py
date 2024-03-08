import pyaudio
import wave


def get_audio_bus():
    if not hasattr(get_audio_bus, "audio_bus"):
        get_audio_bus.audio_bus = AudioBus()

    return get_audio_bus.audio_bus


class AudioBus:
    def __init__(self):
        self._state = "idle"

        self._active_audio_widget = None
        self._active_audio_path = None

        self._audio_recorder = AudioRecorder()
        self._audio_player = AudioPlayer(
            on_finish_callback=self.on_audio_device_finish_callback
        )

        self._on_save_recording_callback = None

    @property
    def state(self):
        return self._state

    @property
    def passed_time(self):
        if self._state == "playing":
            return self._audio_player.playing_time

        if self._state == "recording":
            return self._audio_recorder.recording_length

    @property
    def total_time(self):
        if self._state == "playing":
            return self._audio_player.total_time

        if self._state == "recording":
            return self.passed_time

    def set_on_save_recording_callback(self, callback):
        self._on_save_recording_callback = callback

    def play(self, audio_player_widget, audio_path):
        if self._state == "playing":
            self._audio_player.stop()
        if self._state == "recording":
            self._audio_recorder.stop()

        if self._active_audio_widget is not None:
            self._active_audio_widget.state = "stop"

        self._active_audio_widget = audio_player_widget
        if self._active_audio_widget is not None:
            self._active_audio_widget.state = "play"
        self._audio_player.play(audio_path)

        self._state = "playing"

    def record(self, audio_recorder_widget, audio_path):
        if self._state == "playing":
            self._audio_player.stop()
        if self._state == "recording":
            saved_recording_path = self._audio_recorder.stop()
            if self._on_save_recording_callback is not None and saved_recording_path:
                self._on_save_recording_callback(saved_recording_path)

        if self._active_audio_widget is not None:
            self._active_audio_widget.state = "stop"

        self._active_audio_widget = audio_recorder_widget
        self._audio_recorder.record(audio_path)
        self._active_audio_widget.state = "record"
        self._state = "recording"

    def stop(self, audio_device_widget=None):
        if self._active_audio_widget is not None:
            self._active_audio_widget.state = "stop"

        if self._state == "playing":
            self._audio_player.stop()
            # audio_device_widget.state = "stop"
        if self._state == "recording":
            saved_recording_path = self._audio_recorder.stop()
            if self._on_save_recording_callback is not None and saved_recording_path:
                self._on_save_recording_callback(saved_recording_path)

        if audio_device_widget is not None:
            audio_device_widget.state = "stop"

        self._state = "idle"
        self._active_audio_path = None
        self._active_audio_widget = None

    def on_audio_device_finish_callback(self):
        if self._active_audio_widget is not None:
            self._active_audio_widget.state = "stop"

        self._active_audio_widget = None
        self._state = "idle"


class AudioRecorder:
    # PyAudio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    def __init__(self):
        self._p = pyaudio.PyAudio()
        self._stream = None
        self._frames = []
        self._frame_count = 0
        self._audio_path = None

    @property
    def recording_length(self):
        if self._stream is None or not self._stream.is_active():
            return 0

        return self._frame_count / self.RATE

    def record(self, audio_path):
        self._audio_path = audio_path

        self._frames = []
        self._frame_count = 0

        self._stream = self._p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self._stream_callback,
        )

    def _stream_callback(self, in_data, frame_count, time_info, status):
        self._frames.append(in_data)
        self._frame_count += frame_count

        return in_data, pyaudio.paContinue

    def stop(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()

        with wave.open(self._audio_path, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self._p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b"".join(self._frames))
            wf.close()

        return self._audio_path


class AudioPlayer:
    WARM_UP_ROUNDS = 200

    def __init__(self, on_finish_callback):
        self._on_finish_callback = on_finish_callback

        self._p = pyaudio.PyAudio()
        self._stream = None
        self._frames = []
        self._head_pos = 0
        self._sample_width = 0
        self._num_channels = 0
        self._rate = 0

        self._warm_up_counter = 0  # To avoid audio glitches

    @property
    def playing_time(self):
        if (
            not self._frames
            or not self._rate
            or not self._sample_width
            or not self._num_channels
        ):
            return 0

        return (self._head_pos / (self._sample_width * self._num_channels)) / self._rate

    @property
    def total_time(self):
        if (
            not self._frames
            or not self._rate
            or not self._sample_width
            or not self._num_channels
        ):
            return 0

        return (
            len(self._frames) / (self._sample_width * self._num_channels)
        ) / self._rate

    def play(self, audio_path):
        if not audio_path:
            return

        with wave.open(audio_path, "rb") as wf:
            self._frames = wf.readframes(wf.getnframes())

            self._rate = wf.getframerate()
            self._format = self._p.get_format_from_width(wf.getsampwidth())
            self._sample_width = wf.getsampwidth()
            self._num_channels = wf.getnchannels()

        self._head_pos = 0

        self._warm_up_counter = 0

        self._stream = self._p.open(
            format=self._format,
            channels=self._num_channels,
            rate=self._rate,
            output=True,
            stream_callback=self._stream_callback,
        )

    def _stream_callback(self, in_data, frame_count, time_info, status):
        chunk_size = frame_count * self._sample_width * self._num_channels

        if self._warm_up_counter < self.WARM_UP_ROUNDS:
            print("AudioPlayer._stream_callback", self._warm_up_counter)
            self._warm_up_counter += 1
            return (b"\x00" * chunk_size, pyaudio.paContinue)

        data = self._frames[self._head_pos : self._head_pos + chunk_size]
        self._head_pos += chunk_size

        frame_size = self._sample_width * self._num_channels

        processed_frame_count = int(0 if frame_size == 0 else len(data) / frame_size)

        if processed_frame_count < frame_count:
            self._on_finish_callback()
            self.stop()

            return (data if data else b""), pyaudio.paComplete

        return data, pyaudio.paContinue

    def _reset_params(self):
        self._frames = []
        self._num_total_frames = 0
        self._rate = 0
        self._format = 0
        self._sample_width = 0
        self._num_channels = 0
        self._head_pos = 0

    def stop(self):
        print("AudioPlayer.stop")
        if self._stream is not None:
            self._stream.close()

        self._reset_params()
