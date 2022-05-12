from _04_dialog_manager.event import subscribe, post_event

def handle_stop_event(slots = None):
    """
    posts dialog_manager_output event
    @param slots: empty placeholder
    """
    post_event("dialog_manager_output", "")

def setup_stop_event_handlers():
    """
    subcribes all events 
    """
    subscribe("stop", handle_stop_event)
