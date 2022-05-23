from _04_dialog_manager.event import subscribe, post_event

def handle_dummy_event_a(data):
    """
    dummy event for scalability test,
    uses helper method to post dialog_manager_output event
    """
    post_event_dm_output("Dummy event a erkannt")

def handle_dummy_event_b(data):
    """
    dummy event for scalability test,
    uses helper method to post dialog_manager_output event
    """
    post_event_dm_output("Dummy event b erkannt")

def handle_dummy_event_c(data):
    """
    dummy event for scalability test,
    uses helper method to post dialog_manager_output event
    """
    post_event_dm_output("Dummy event c erkannt")

def post_event_dm_output(response):
    post_event("dialog_manager_output", response)

def setup_dummy_event_handler():
    """
    subcribes all events 
    """
    subscribe("dummy_a", handle_dummy_event_a)
    subscribe("dummy_b", handle_dummy_event_b)
    subscribe("dummy_c", handle_dummy_event_c)
