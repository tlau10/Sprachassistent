from _04_dialog_manager.event import subscribe
from voice_assistant_helper import append_to_file
from decouple import config

def handle_dialog_manager_output_event(data):
    """
    appends given text to output file
    @param data: text to write to file
    """
    dialog_manager_output_path = config('DIALOG_MANAGER_OUTPUT_PATH')
    append_to_file(file_path = dialog_manager_output_path, text = data)

def setup_dialog_manager_events():
    """
    subcribes all events 
    """
    subscribe("dialog_manager_output", handle_dialog_manager_output_event)
