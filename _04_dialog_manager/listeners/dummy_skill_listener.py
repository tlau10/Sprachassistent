from _04_dialog_manager.event import subscribe, post_event

def handle_dummy_event_a(data):
    """
    dummy event for scalability test,
    posts dialog_manager_output event
    """
    response = f"Dummy event a erkannt"
    post_event("dialog_manager_output", response)

def setup_dummy_event_handler():
    """
    subcribes all events 
    """
    subscribe("dummy_a", handle_dummy_event_a)
