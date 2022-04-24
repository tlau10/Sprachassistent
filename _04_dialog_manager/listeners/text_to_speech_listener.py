from _04_dialog_manager.event import subscribe
from _05_text_to_speech.text_to_speech import TextToSpeech

def handle_text_to_speech_event(data):
    """
    runs text-to-speech
    @param data: text to translate into audio
    """
    tts = TextToSpeech()
    tts.start(data)

def setup_text_to_speech_event_handlers():
    """
    subcribes all events 
    """
    subscribe("text_to_speech", handle_text_to_speech_event)
