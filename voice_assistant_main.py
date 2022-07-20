import subprocess
from decouple import config
from _01_wake_word_detection.wake_word_detection import WakeWordDetection
from _02_speech_to_text.speech_to_text import SpeechToText
from _03_natural_language_understanding.natural_language_understanding import NLU
from _04_dialog_manager.dialog_manager import DialogManager
from _05_text_to_speech.text_to_speech import TextToSpeech

class VoiceAssistant:

    def __init__(self):
        self.wake_word_detection = WakeWordDetection()
        self.speech_to_text = SpeechToText()
        self.nlu = NLU()
        self.dialog_manager = DialogManager()
        self.text_to_speech = TextToSpeech()

    def run(self):
        """
        runs voice assistant in endless loop
        """
        while True:
            self.wake_word_detection.start()
            self.speech_to_text.start()
            self.nlu.start()
            self.dialog_manager.start()
            self.text_to_speech.start()
            self.data_cleanup()

    def start_bot(self):
        """
        starts voice assistant bot in a new Process
        """
        cmd = f"python {config('BOT')}"
        with subprocess.Popen(cmd, shell = True):
            pass

    def data_cleanup(self):
        """
        removes all generated files after the user request is done
        """
        subprocess.run(["rm", "-f", config('DIALOG_MANAGER_OUTPUT_PATH'), \
            config('STT_OUTPUT_PATH'), config('NLU_OUTPUT_PATH'), config('TTS_OUTPUT_PATH')], \
                check = True)

if __name__ == "__main__":
    voice_assistant = VoiceAssistant()
    voice_assistant.start_bot()
    voice_assistant.run()
