from decouple import config
from _04_dialog_manager.event import subscribe

def handle_none_event(slots = None):
    """
    handles none intent
    @param slots: empty placeholder
    @return: response text
    """
    response = "Ich kann dir leider nicht weiterhelfen"
    return response

def setup_none_event_handlers():
    """
    subcribes all events
    """
    subscribe("none", handle_none_event)
