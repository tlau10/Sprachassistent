import pvporcupine
from voice_assistant_helper import get_next_audio_frame, play_notification_sound, read_key_file
from datetime import datetime
from decouple import config
import os

class WakeWordDetection:
    def __init__(self):
        access_key = read_key_file(config('PICOVOICE_ACCESS_KEY_PATH'))

        if os.uname()[4].startswith("arm"):
            keyword_file_path = config('PORCUPINE_KEYWORD_PATH_PI')
        else:
            keyword_file_path = config('PORCUPINE_KEYWORD_PATH_LINUX')

        model_file_path = config('PORCUPINE_MODEL_PATH')
        self.porcupine = Porcupine(access_key=access_key, keyword_file_path=keyword_file_path, model_file_path=model_file_path)

    def start(self):
        """
        start listening to audio stream and look for defined wake word
        """

        print("wake word detection listening on audio input...")
        rate = self.porcupine.engine.sample_rate
        frame_length = self.porcupine.engine.frame_length

        while True:
            audio_frame = get_next_audio_frame(sample_rate = rate, frames = frame_length)
            keyword_index = self.porcupine.engine.process(audio_frame)

            if keyword_index == 0:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"wake word detected: {timestamp}")
                play_notification_sound(config('WWD_NOTIFICATION'))

class Porcupine:
    def __init__(self, access_key, keyword_file_path, model_file_path):
        self.access_key = access_key
        self.keyword_file_path = keyword_file_path
        self.model_file_path = model_file_path

        self.engine = pvporcupine.create(
            access_key = self.access_key,
            keyword_paths = [keyword_file_path],
            model_path = self.model_file_path
        )