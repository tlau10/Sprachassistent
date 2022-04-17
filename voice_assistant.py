from _01_wake_word_detection.wake_word_detection import WakeWordDetection
from _03_natural_language_understanding.natural_language_understanding import NLU
import os

wake_word_detection = WakeWordDetection()
wake_word_detection.start()

os.system('python3 _02_speech_to_text/mic_vad_streaming.py\
    --model _02_speech_to_text/model.pbmm\
    --scorer _02_speech_to_text/de-aashishag-1-prune-kenlm.scorer\
    --savewav _02_speech_to_text/stt_audio')

nlu = NLU()
nlu.train()
nlu.parse()