import deepspeech
import os
from decouple import config
from voice_assistant_helper import get_next_audio_frame
import time

class SpeechToText:
    def __init__(self):
        if os.uname()[4].startswith("arm"):
            model_file_path = config('DEEPSPEECH_MODEL_PATH_DE_PI')
        else:
            model_file_path = config('DEEPSPEECH_MODEL_PATH_DE_LINUX')

        self.deep_speech_engine_de = DeepSpeech(model_file_path = model_file_path)

    def start(self):
        stream = self.deep_speech_engine_de.create_stream()
        sample_rate = self.deep_speech_engine_de.get_sample_rate()
        frames = self.deep_speech_engine_de.get_beam_width()
        timeout = time.time() + 5
        print("start text-to-speech...")
        while True:
            audio_frame = get_next_audio_frame(sample_rate = sample_rate, frames = frames)
            stream.feedAudioContent(audio_frame)
            if time.time() > timeout:
                break
        stt_result = stream.finishStream()
        print(f"result of stt: {stt_result}")

class DeepSpeech(deepspeech.Model):
    def __init__(self, model_file_path):
        super().__init__(model_file_path)
        super().enableExternalScorer(config('DEEPSPEECH_SCORER_PATH_DE'))

    def create_stream(self):
        """
        creates streaming inference state
        @return: stream object
        """
        return super().createStream()

    def get_sample_rate(self):
        return super().sampleRate()
    
    def get_beam_width(self):
        return super().beamWidth()
