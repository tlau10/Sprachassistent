from listeners.none_skill_listener import setup_none_event_handlers
from listeners.text_to_speech_listener import setup_text_to_speech_event_handlers
from listeners.stop_skill_listener import setup_stop_event_handlers
from listeners.wikipedia_skill_listener import setup_wikipedia_event_handlers

def setup_event_handlers():
    """
    calls all setup functions of available skill listeners
    """
    setup_none_event_handlers()
    setup_text_to_speech_event_handlers()
    setup_stop_event_handlers()
    setup_wikipedia_event_handlers()
