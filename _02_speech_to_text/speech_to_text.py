from deepspeech import Model
import os
from decouple import config

class SpeechToText:
    def __init__(self):
        if os.uname()[4].startswith("arm"):
            model_file_path = config('DEEPSPEECH_MODEL_PATH_DE_PI')
        else:
            model_file_path = config('DEEPSPEECH_MODEL_PATH_DE_LINUX')

        self.deep_speech_engine_de = DeepSpeech(model_file_path = model_file_path)

class DeepSpeech:
    def __init__(self, model_file_path):
        self.stt_model = Model(model_file_path)