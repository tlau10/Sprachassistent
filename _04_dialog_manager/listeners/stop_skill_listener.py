from _04_dialog_manager.event import subscribe, post_event

def handle_stop_event(data):
    """
    posts text-to-speech event
    @param data: empty placeholder
    """
    post_event("text_to_speech", "")

def setup_stop_event_handlers():
    """
    subcribes all events 
    """
    subscribe("stop", handle_stop_event)
