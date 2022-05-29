from voice_assistant_helper import write_json_file, read_json_file
from decouple import config

JSON_FILE_OUTPUT_PATH = config('BOT_ENTRIES')

def store_entry(entry):
    """
    writes new entry to json file
    @param entry: entry to write to file as tuple(intent, slot, replied_message, improved_message)
    """
    intent, slot, recognized_value, improved_value = entry
    print(f"intent: {intent}, slot: {slot}, recognized_value: {recognized_value}, improved_value: {improved_value}")

    # read json
    entries = read_json_file(file_path = JSON_FILE_OUTPUT_PATH)

    # retrieve entry
    entry = entries[intent][slot]

    # get first index from list entry with matching key
    try:
        key_index = next(i for i,d in enumerate(entry['values']) if recognized_value in d)
    except StopIteration as e:
        key_index = None

    # update existing entry
    if key_index is not None:
        entry['values'][key_index] = {recognized_value : improved_value}
    # append new key value pair
    else:
        entry['values'].append({recognized_value : improved_value})

    write_json_file(file_path = JSON_FILE_OUTPUT_PATH, json_object = entries)
