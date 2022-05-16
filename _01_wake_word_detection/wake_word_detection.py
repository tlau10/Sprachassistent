import pvporcupine
from voice_assistant_helper import get_next_audio_frame, play_notification_sound, read_from_file
from datetime import datetime
from decouple import config
import os

class WakeWordDetection:

    def __init__(self):
        access_key = read_from_file(config('PICOVOICE_ACCESS_KEY_PATH'))

        if os.uname().machine == "x86_64":
            keyword_path = config('PORCUPINE_KEYWORD_PATH_LINUX')
        else:
            keyword_path = config('PORCUPINE_KEYWORD_PATH_PI')

        model_path = config('PORCUPINE_MODEL_PATH')
        self.porcupine = Porcupine(
            access_key = access_key,
            keyword_path = keyword_path,
            model_path = model_path
        )

    def start(self):
        """
        start listening to audio stream and look for defined wake word,
        plays notification sound on detected wake word
        """
        print("wake word detection listening on audio input...")

        if os.uname().machine == "x86_64":
            rate = self.porcupine.engine.sample_rate
        else:
            rate = 48000

        frame_length = self.porcupine.engine.frame_length

        while True:
            audio_frame = get_next_audio_frame(sample_rate = rate, frames = frame_length)
            keyword_index = self.porcupine.engine.process(audio_frame)

            if keyword_index == 0:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"wake word detected: {timestamp}")
                play_notification_sound(config('WWD_NOTIFICATION'))
                return

class Porcupine:

    def __init__(self, access_key, keyword_path, model_path):
        self.access_key = access_key
        self.keyword_path = keyword_path
        self.model_path = model_path

        self.engine = pvporcupine.create(
            access_key = self.access_key,
            keyword_paths = [keyword_path],
            model_path = self.model_path
        )