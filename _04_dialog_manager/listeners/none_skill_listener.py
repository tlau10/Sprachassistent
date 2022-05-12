from _04_dialog_manager.event import subscribe, post_event

def handle_none_event(slots = None):
    """
    posts text-to-speech event
    @param slots: empty placeholder
    """
    response = "Ich kann dir leider nicht weiterhelfen"
    post_event("dialog_manager_output", response)

def setup_none_event_handlers():
    """
    subcribes all events 
    """
    subscribe("none", handle_none_event)
