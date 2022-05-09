from _04_dialog_manager.event import subscribe, post_event

def handle_menue_search_event(data):
    pass

def setup_mensa_event_handlers():
    """
    subscribes all events
    """
    subscribe("search_menue", handle_menue_search_event)
