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
    def frame_count(self):
        return self._frame_count

    def open_stream(self):
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

    def close(self):
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

    def play(self, frames):
        self._stream = self._p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True,
            stream_callback=self._stream_callback,
        )

    def _stream_callback(self, in_data, frame_count, time_info, status):
        print("Playing:", in_data, frame_count, time_info, status)
        return in_data, pyaudio.paContinue

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
