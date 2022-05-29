from _04_dialog_manager.event import subscribe

def handle_learning_event(slots):
    """
    @param slots: empty placeholder
    """
    pass

def setup_bot_event_handlers():
    """
    subcribes all events 
    """
    subscribe("learn", handle_learning_event)