"""
Partly taken from Mozilla DeepSpeech
GitHub repository:
https://github.com/mozilla/DeepSpeech-examples/blob/r0.9/mic_vad_streaming/README.rst
"""
import logging
import collections
import queue
import platform
import wave
import deepspeech
import numpy as np
import pyaudio
import webrtcvad
from halo import Halo
from scipy import signal
from decouple import config

logging.basicConfig(level=20)

class SpeechToText:

    def __init__(self):

        if platform.system() == "Linux" or platform.system() == "Windows":
            model_path = config('STT_MODEL_PATH')
        else:
            model_path = config('STT_MODEL_PATH_PI')

        scorer_path = config('STT_SCORER_PATH')

        self.deep_speech = DeepSpeech(
            model_path = model_path,
            scorer_path = scorer_path,
            text_output_path = None)

    def start(self):
        """
        start streaming audio using vad
        @return: recognized phrase
        """
        if platform.system() == "Linux" or platfrom.system() == "Windows":
            rate = 16000
        else:
            rate = 48000

        # Start audio with VAD
        vad_audio = VADAudio(
            aggressiveness = 3,
            device = None,
            input_rate = rate,
            file = None
        )
        print("speech-to-text listening...")
        frames = vad_audio.vad_collector()

        # Stream from microphone to DeepSpeech using VAD
        spinner = Halo(spinner='line')
        stream_context = self.deep_speech.engine.createStream()
        for frame in frames:
            if frame is not None:
                if spinner:
                    spinner.start()
                logging.debug("streaming frame")
                stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
            else:
                if spinner:
                    spinner.stop()
                logging.debug("end utterence")
                text = stream_context.finishStream()
                print(f"speech-to-text recognized: {text}")
                return text

class DeepSpeech:

    def __init__(self, model_path, scorer_path, text_output_path):
        self.model_path = model_path
        self.scorer_path = scorer_path
        self.text_output_path = text_output_path

        self.engine = deepspeech.Model(
            model_path = self.model_path
        )
        self.engine.enableExternalScorer(scorer_path = self.scorer_path)

class Audio:
    """Streams raw audio from microphone. Data is received in a separate thread,
    and stored in a buffer, to be read from."""

    FORMAT = pyaudio.paInt16
    # Network/VAD rate-space
    RATE_PROCESS = 16000
    CHANNELS = 1
    BLOCKS_PER_SECOND = 50

    def __init__(self, callback=None, device=None, input_rate=RATE_PROCESS, file=None):
        def proxy_callback(in_data, *unused):
            if self.chunk is not None:
                in_data = self.wave_file.readframes(self.chunk)
            callback(in_data)
            return (None, pyaudio.paContinue)
        if callback is None:
            callback = lambda in_data: self.buffer_queue.put(in_data)
        self.buffer_queue = queue.Queue()
        self.device = device
        self.input_rate = input_rate
        self.sample_rate = self.RATE_PROCESS
        self.block_size = int(self.RATE_PROCESS / float(self.BLOCKS_PER_SECOND))
        self.block_size_input = int(self.input_rate / float(self.BLOCKS_PER_SECOND))
        self.pyaudio = pyaudio.PyAudio()

        kwargs = {
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size_input,
            'stream_callback': proxy_callback,
        }

        self.chunk = None
        # if not default device
        if self.device:
            kwargs['input_device_index'] = self.device
        elif file is not None:
            self.chunk = 320
            self.wave_file= wave.open(file, 'rb')

        self.stream = self.pyaudio.open(**kwargs)
        self.stream.start_stream()

    def resample(self, data):
        """
        Microphone may not support our native processing sampling rate, so
        resample from input_rate to RATE_PROCESS here for webrtcvad and
        deepspeech

        Args:
            data (binary): Input audio stream
            input_rate (int): Input audio rate to resample from
        """
        data16 = np.fromstring(string=data, dtype=np.int16)
        resample_size = int(len(data16) / self.input_rate * self.RATE_PROCESS)
        resample = signal.resample(data16, resample_size)
        resample16 = np.array(resample, dtype=np.int16)
        return resample16.tostring()

    def read_resampled(self):
        """Return a block of audio data resampled to 16000hz, blocking if necessary."""
        return self.resample(data=self.buffer_queue.get())

    def read(self):
        """Return a block of audio data, blocking if necessary."""
        return self.buffer_queue.get()

    def destroy(self):
        """closes pyaudio stream"""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

    frame_duration_ms = property(lambda self: 1000 * self.block_size // self.sample_rate)

    def write_wav(self, filename, data):
        """
        writes data to wav file
        @param filename: name of file
        @param data: audio data to write to file
        """
        logging.info("write wav %s", filename)
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(self.CHANNELS)
        assert self.FORMAT == pyaudio.paInt16
        wave_file.setsampwidth(2)
        wave_file.setframerate(self.sample_rate)
        wave_file.writeframes(data)
        wave_file.close()


class VADAudio(Audio):
    """Filter & segment audio with voice activity detection."""

    def __init__(self, aggressiveness=3, device=None, input_rate=None, file=None):
        super().__init__(device=device, input_rate=input_rate, file=file)
        self.vad = webrtcvad.Vad(aggressiveness)

    def frame_generator(self):
        """Generator that yields all audio frames from microphone."""
        if self.input_rate == self.RATE_PROCESS:
            while True:
                yield self.read()
        else:
            while True:
                yield self.read_resampled()

    def vad_collector(self, padding_ms=300, ratio=0.75, frames=None):
        """Generator that yields series of consecutive audio frames comprising each utterence,
        separated by yielding a single None.
        Determines voice activity by ratio of frames in padding_ms.
        Uses a buffer to include padding_ms prior to being triggered.
            Example: (frame, ..., frame, None, frame, ..., frame, None, ...)
                      |---utterence---|        |---utterence---|
        """
        if frames is None:
            frames = self.frame_generator()
        num_padding_frames = padding_ms // self.frame_duration_ms
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False

        for frame in frames:
            if len(frame) < 640:
                return

            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > ratio * ring_buffer.maxlen:
                    triggered = True
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()

            else:
                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > ratio * ring_buffer.maxlen:
                    triggered = False
                    yield None
                    ring_buffer.clear()
