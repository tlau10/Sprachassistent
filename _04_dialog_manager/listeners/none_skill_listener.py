from _04_dialog_manager.event import subscribe
from decouple import config
from voice_assistant_helper import write_to_file

def handle_none_event(slots = None):
    """
    writes output to file
    @param slots: empty placeholder
    """
    response = "Ich kann dir leider nicht weiterhelfen"
    write_to_file(file_path = config('DIALOG_MANAGER_OUTPUT_PATH'), text = response)

def setup_none_event_handlers():
    """
    subcribes all events 
    """
    subscribe("none", handle_none_event)
