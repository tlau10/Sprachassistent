from decouple import config
from picotts import PicoTTS
import multiprocessing
from playsound import playsound

class TextToSpeech:
    
    def __init__(self):
        self.picotts = PicoTTS_(language = 'de-DE')
        self.wav_output_path = config('TTS_OUTPUT_PATH')

    def start(self, text):
        """
        generates wav file from given text then plays wav in a new process
        @param text: text to translate into audio
        """
        audio = self.picotts.engine.synth_wav(text)
        with open(config('TTS_OUTPUT_PATH'), mode = 'bw') as wav:
            wav.write(audio)

        process = multiprocessing.Process(target=playsound, args=(self.wav_output_path, ))
        process.start()

class PicoTTS_:

    def __init__(self, language):
        self.engine = PicoTTS()
        self.engine.voice = language