from _01_wake_word_detection.wake_word_detection import WakeWordDetection
from _02_speech_to_text.speech_to_text import SpeechToText
from _03_natural_language_understanding.natural_language_understanding import NLU
from _04_dialog_manager.dialog_manager import DialogManager

# init
wake_word_detection = WakeWordDetection()
speech_to_text = SpeechToText()
nlu = NLU()
dialog_manager = DialogManager()

while True:
    wake_word_detection.start()

    speech_to_text.start()

    nlu.start()

    dialog_manager.start()
