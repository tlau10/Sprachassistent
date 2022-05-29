from _04_dialog_manager.event import subscribe

def handle_start_learning_event(slots):
    """
    @param slots: empty placeholder
    """
    pass

def setup_bot_event_handlers():
    """
    subcribes all events 
    """
    subscribe("start_learning", handle_start_learning_event)