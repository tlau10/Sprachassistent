from pickle import TRUE
from _01_wake_word_detection.wake_word_detection import WakeWordDetection
from _03_natural_language_understanding.natural_language_understanding import NLU
from _04_dialog_manager.dialog_manager import DialogManager
import subprocess
from decouple import config

# init
wake_word_detection = WakeWordDetection()
nlu = NLU()
dialog_manager = DialogManager()

while TRUE:
    wake_word_detection.start()

    subprocess.call(['python3', '_02_speech_to_text/mic_vad_streaming.py',
    '--model', config('STT_MODEL_PATH'), '--scorer', config('STT_SCORER_PATH'),
    '--savewav', config('STT_WAV_OUTPUT_PATH')])

    nlu.train()
    nlu.parse()

    dialog_manager.start()
