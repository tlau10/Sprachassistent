from decouple import config
from voice_assistant_helper import append_to_file, read_from_file_by_line
from _04_dialog_manager.event import subscribe
from _04_dialog_manager.manual_learning.voice_assistant_bot_helper import \
    extract_slots_and_convert_to_dict, generate_request_string

DIALOG_MANAGER_DATA = config('DIALOG_MANAGER_DATA_PATH')
REQUEST_OUTPUT_FILE = config('BOT_REQUESTS')
TIME_LIMIT = 10.0

def handle_start_learning_event(scenario = None):
    """
    uses dialog_manager_data.txt to decide if request needs to be made then stores it in file
    covers the following scenarios
    scenario 1: last line is stop intent and <= time_limit to second last
    scenario 2: last two lines are from same intent and <= time_limit to second last
    scenario 3: nothing was found for slot value
    in all scenarios: write request for each slot to requests.txt
    @param scenario: scenario from which event was startet
    """
    lines = read_from_file_by_line(file_path = DIALOG_MANAGER_DATA)

    # check if entries exist
    if len(lines) == 0:
        return

    # get last line
    last_line_parts = lines[-1].split(" ")

    # scenario 1: last line is stop intent and <= time_limit to second last
    if scenario == 1 and len(lines) >= 2:
        print("scenario 1 started...")
        slots = extract_slots_and_convert_to_dict(string = lines[-2])
    # scenario 2: last two lines are from same intent and <= time_limit to second last
    elif scenario == 2 and len(lines) >= 2:
        print("scenario 2 started...")
        slots = extract_slots_and_convert_to_dict(string = lines[-1])
    # scenario 3: nothing was found for slot value
    elif scenario == 3 and len(lines) >= 1:
        print("scenario 3 started...")
        slots = extract_slots_and_convert_to_dict(string = lines[-1])

        # no slot values found therefore nothing to improve
        if len(slots) == 0:
            return

        # generate request string and append it to file
        requests = generate_request_string(data = (last_line_parts[0], slots))
        for request in requests:
            append_to_file(file_path = REQUEST_OUTPUT_FILE, text = f"{request}\n")
        return
    # invalid scenario
    else:
        return

    # no slot values found therefore nothing to improve
    if len(slots) == 0:
        return

    # get second last line
    second_last_line_parts = lines[-2].split(" ")

    # calculate time difference
    time_diff = float(last_line_parts[-1]) - float(second_last_line_parts[-1])

    # check time difference below set time limit
    if time_diff <= TIME_LIMIT:
        # generate request string and append it to file
        requests = generate_request_string(data = (second_last_line_parts[0], slots))
        for request in requests:
            append_to_file(file_path = REQUEST_OUTPUT_FILE, text = f"{request}\n")

def setup_bot_event_handlers():
    """
    subcribes all events
    """
    subscribe("start_learning", handle_start_learning_event)
