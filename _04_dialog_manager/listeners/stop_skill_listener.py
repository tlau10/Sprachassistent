from _04_dialog_manager.event import post_event, subscribe

def handle_stop_event(slots = None):
    """
    handles stop intent
    @param slots: empty placeholder
    @return: empty response
    """
    ###Learning###
    post_event("start_learning", 1)
    ###Learning###

    return ""

def setup_stop_event_handlers():
    """
    subcribes all events
    """
    subscribe("stop", handle_stop_event)
