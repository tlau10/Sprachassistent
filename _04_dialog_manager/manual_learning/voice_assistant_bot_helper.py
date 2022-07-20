import re
from decouple import config
from voice_assistant_helper import write_json_file, read_json_file, read_from_file_by_line, \
    convert_string_to_dict

JSON_FILE_OUTPUT_PATH = config('BOT_ENTRIES')
DIALOG_MANAGER_DATA = config('DIALOG_MANAGER_DATA_PATH')

def store_entry(entry):
    """
    writes new entry to json file
    @param entry: entry to write to file as tuple(intent, slot, replied_message, improved_message)
    """
    intent, slot, recognized_value, improved_value = entry
    print(f"intent: {intent}, slot: {slot}, recognized_value: {recognized_value}, \
        improved_value: {improved_value}")

    # read json
    entries = read_json_file(file_path = JSON_FILE_OUTPUT_PATH)

    # retrieve entry
    entry = entries[intent][slot]

    # get first index from list entry with matching key
    try:
        key_index = next(i for i,d in enumerate(entry['values']) if recognized_value in d)
    except StopIteration:
        key_index = None

    # update existing entry
    if key_index is not None:
        entry['values'][key_index] = {recognized_value : improved_value}
    # append new key value pair
    else:
        entry['values'].append({recognized_value : improved_value})

    write_json_file(file_path = JSON_FILE_OUTPUT_PATH, json_object = entries)

def lookup_entry():
    """
    looks for slot value in entries
    @return: returns found entry otherwise None
    """
    # get last line
    lines = read_from_file_by_line(file_path = DIALOG_MANAGER_DATA)
    last_line_parts = lines[-1].split(" ")

    # extract slots
    slots = extract_slots_and_convert_to_dict(string = lines[-1])

    # read json
    entries = read_json_file(file_path = JSON_FILE_OUTPUT_PATH)

    # retrieve entry
    intent = last_line_parts[0]
    first_key = next(iter(slots)) # gets first key from dict
    first_key_value = slots[first_key]
    entry = entries[intent][first_key]

    # get first index from list entry with matching key
    try:
        key_index = next(i for i,d in enumerate(entry['values']) if first_key_value in d)
        slot_entry = entry['values'][key_index]

        new_slot_value = slot_entry[first_key_value]
        return new_slot_value
    except StopIteration:
        key_index = None

def generate_request_string(data):
    """
    generates request string
    @param data: tuple (intent, slots as dict)
    @return: request string for each slot
    """
    intent, slots = data
    requests = list()
    for key, value in slots.items():
        requests.append(f"{intent} {key} {value}")

    return requests

def extract_slots_and_convert_to_dict(string):
    """
    extracts slot values from given string then call convert_string_to_dict()
    @param string: string to extract slots from
    @return: dict of slots
    """
    slots = re.search("{.*}", string).group(0)
    return convert_string_to_dict(string = slots)
