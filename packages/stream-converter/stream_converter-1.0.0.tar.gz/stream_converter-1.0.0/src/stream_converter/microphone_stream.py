import pyaudio
from typing import Optional, Self, Generator


def get_microphone_stream_generator() -> Generator[bytes, None, None]:
    audio = pyaudio.PyAudio()
    frames_per_buffer = 1024
    microphone_stream = audio.open(
        format=pyaudio.paFloat32,             # audio format (e.g., paFloat32 for float32)
        channels=1,                           # number of audio channels
        rate=44100,                           # bit rate (samples per second)
        frames_per_buffer=frames_per_buffer,  # number of frames per buffer
        input=True,
    )

    try:
        while True:
            yield microphone_stream.read(frames_per_buffer, exception_on_overflow=False)
    finally:
        microphone_stream.stop_stream()
        microphone_stream.close()
        audio.terminate()


class MicrophoneStream:
    def __init__(
        self,
        format: int = pyaudio.paFloat32,
        channels: int = 1,
        rate: int = 44100,
        frames_per_buffer: int = 1024,
    ) -> None:
        self.format: int = format
        self.channels: int = channels
        self.rate: int = rate
        self.frames_per_buffer: int = frames_per_buffer
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.format,                        # audio format (e.g., paFloat32 for float32)
            channels=self.channels,                    # number of audio channels
            rate=self.rate,                            # bit rate (samples per second)
            frames_per_buffer=self.frames_per_buffer,  # number of frames per buffer
            input=True,
        )

    def read(self) -> bytes:
        return self.stream.read(self.frames_per_buffer, exception_on_overflow=False)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[object],
    ) -> None:
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
