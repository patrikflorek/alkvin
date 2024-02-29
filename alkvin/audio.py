import pyaudio
import wave

# PyAudio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


class AudioRecorder:
    def __init__(self):
        self._p = pyaudio.PyAudio()
        self._stream = None
        self._frames = []
        self._frame_count = 0

    @property
    def frames(self):
        return self._frames

    @property
    def time(self):
        if self._stream is None or not self._stream.is_active():
            return 0

        return self._frame_count // RATE

    def record(self):
        self._frame_count = 0

        self._stream = self._p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self._stream_callback,
        )

    def _stream_callback(self, in_data, frame_count, time_info, status):
        self._frames.append(in_data)
        self._frame_count += frame_count

        return in_data, pyaudio.paContinue

    def stop(self):
        if self._stream is None:
            return

        self._stream.stop_stream()
        self._stream.close()

    def save(self, file_path):
        wf = wave.open(file_path, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self._p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(self._frames))
        wf.close()


class AudioPlayer:
    def __init__(self):
        self._p = pyaudio.PyAudio()
        self._stream = None
        self._wf = None

    @property
    def time(self):
        if self._stream is None or not self._stream.is_active():
            return 0

        return self._stream.get_time()

    def play(self, audio_path):
        if not audio_path:
            return

        if self._wf is not None:
            self._wf.close()

        if self._stream is not None and self._stream.is_active():
            self._stream.close()

        print(f"Playing {audio_path}")
        self._wf = wave.open(audio_path, "rb")

        self._stream = self._p.open(
            format=self._p.get_format_from_width(self._wf.getsampwidth()),
            channels=self._wf.getnchannels(),
            rate=self._wf.getframerate(),
            output=True,
            stream_callback=self._stream_callback,
        )

    def _stream_callback(self, in_data, frame_count, time_info, status):
        data = self._wf.readframes(frame_count)
        return data, pyaudio.paContinue

    def stop(self):
        if self._stream is None:
            return

        self._stream.close()
