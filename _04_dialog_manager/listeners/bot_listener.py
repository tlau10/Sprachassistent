from _04_dialog_manager.event import subscribe
from voice_assistant_helper import append_to_file, read_from_file_by_line, convert_string_to_dict
from decouple import config
import re

DIALOG_MANAGER_DATA = config('DIALOG_MANAGER_DATA_PATH')
REQUEST_OUTPUT_FILE = config('BOT_REQUESTS')

def handle_start_learning_event(slots = None):
    """
    @param slots: empty placeholder
    """
    # get last two lines from dm_data.txt
    lines = read_from_file_by_line(file_path = DIALOG_MANAGER_DATA)

    # delete file

    parts_last_line = lines[-1].split(" ")
    parts_second_last_line = lines[-2].split(" ")
    # scenario 1: last line is stop intent and <= 5 sec. to second last then write request to requests.txt
    if 'stop' in parts_last_line:
        diff = float(parts_last_line[-1]) - float(parts_second_last_line[-1])
        if diff <= 5.0:
            slots = re.search("{.*}", lines[-2]).group(0)
            result = convert_string_to_dict(string = slots)
            print(result)
            requests = generate_request_string((parts_second_last_line[0], result))
            for request in requests:
                append_to_file(file_path = REQUEST_OUTPUT_FILE, text = f"{request}\n")
    # scenario 2: last two lines are from same intent and <= 5 sec. to second last then write request for each slot to requests.txt
    # scenario 3: invalid slot value -> gets called by lookup_entry(): only look at latest line and write request for ech slot to requests.txt

def generate_request_string(data):
    """
    @param data: tuple (intent, slots as dict)
    @return: request string for each slot
    """
    intent, slots = data
    requests = list()
    print(slots)
    for key, value in slots.items():
        requests.append(f"{intent} {key} {value}")

    return requests

def handle_lookup_entry_event(slots = None):
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

if __name__ == "__main__":
    handle_start_learning_event()
