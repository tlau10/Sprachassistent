from _04_dialog_manager.event import subscribe
from voice_assistant_helper import append_to_file, read_from_file_by_line, convert_string_to_dict
from decouple import config
import re

DIALOG_MANAGER_DATA = config('DIALOG_MANAGER_DATA_PATH')
REQUEST_OUTPUT_FILE = config('BOT_REQUESTS')
TIME_LIMIT = 5.0

def handle_start_learning_event(slots = None):
    """
    uses dialog_manager_data.txt to decide if request needs to be made then stores it in file
    covers the following scenarios
    scenario 1: last line is stop intent and <= 5 sec. to second last
    scenario 2: last two lines are from same intent and <= 5 sec. to second last
    scenario 3: nothing was found for slot value -> gets called by lookup_entry event, only look at latest line
    in all scenarios: write request for each slot to requests.txt
    @param slots: empty placeholder
    """
    # get last two lines from dm_data.txt
    lines = read_from_file_by_line(file_path = DIALOG_MANAGER_DATA)

    # delete file

    last_line_parts = lines[-1].split(" ")
    second_last_line_parts = lines[-2].split(" ")

    stop_event = False
    # check if last line ist stop event
    if 'stop' in last_line_parts:
        stop_event = True

    time_diff = float(last_line_parts[-1]) - float(second_last_line_parts[-1])
    if time_diff <= TIME_LIMIT:
        # filter out slots and convert it to a dict
        slots = re.search("{.*}", lines[-2] if stop_event else lines[-1]).group(0)
        result = convert_string_to_dict(string = slots)
        print(result)

        # generate request string and append it to file
        requests = generate_request_string((second_last_line_parts[0], result))
        for request in requests:
            append_to_file(file_path = REQUEST_OUTPUT_FILE, text = f"{request}\n")

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
