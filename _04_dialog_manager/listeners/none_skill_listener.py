from _04_dialog_manager.event import subscribe, post_event

def handle_none_event(data):
    """
    posts text-to-speech event
    @param data: empty placeholder
    """
    response = "Ich kann dir leider nicht weiterhelfen"
    post_event("text_to_speech", response)

def setup_none_event_handlers():
    """
    subcribes all events 
    """
    subscribe("none", handle_none_event)
