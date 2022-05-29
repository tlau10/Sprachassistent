from _04_dialog_manager.event import subscribe

def handle_start_learning_event(slots):
    """
    @param slots: empty placeholder
    """
    # get last two lines from dm_data.txt and delete rest
    # scenario 1: last line is stop intent and <= 5 sec. then write request to requests.txt
    # scenario 2: last two lines are from same intent and <= 5 sec. then write request for each slot to requests.txt
    # scenario 3: invalid slot value -> gets called by lookup_entry(): only look at latest line and write request for ech slot to requests.txt
    pass

def handle_lookup_entry_event(slots):
    """
    @param slots: empty placeholder
    """
    # return found entry, if nothing is found call handle_start_learning
    pass

def setup_bot_event_handlers():
    """
    subcribes all events 
    """
    subscribe("start_learning", handle_start_learning_event)
    subscribe("lookup_entry", handle_lookup_entry_event)