from smtplib import SMTPConnectError
from _01_wake_word_detection.wake_word_detection import WakeWordDetection
import os

wake_word_detection = WakeWordDetection()
#wake_word_detection.start()

#speech_to_text = SpeechToText()
#speech_to_text.start()

os.system('python3 _02_speech_to_text/mic_vad_streaming.py\
    --model _02_speech_to_text/.venv/model.pbmm\
    --scorer _02_speech_to_text/.venv/de-aashishag-1-prune-kenlm.scorer\
    --savewav _02_speech_to_text/stt_audio')

