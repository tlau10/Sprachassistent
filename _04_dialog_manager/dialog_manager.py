from _04_dialog_manager.event import post_event
from _04_dialog_manager.observer import setup_event_handlers
from voice_assistant_helper import read_json_file, append_to_file
from decouple import config
import time

class DialogManager:

    def __init__(self):
        # setup all event handlers
        setup_event_handlers()

    def start(self):
        """
        reads json file from nlu, extracts data and calls execute method depending on found intent
        """
        intent = read_json_file(file_path = config('NLU_OUTPUT_PATH'))

        intent_name = intent['intent']['intentName']
        slots = intent['slots']

        # store slot values in dict 'slotname' : 'slotvalue'
        slot_values = dict()
        for slot in slots:
            slot_values[slot['slotName']] = slot['value']['value']

        # no intent matched
        if not intent_name:
            post_event("none", slot_values)
            return

        ###Learning###
        request = f"{intent_name} {str(slot_values)} {time.time()}\n"
        append_to_file(file_path = config('DIALOG_MANAGER_DATA_PATH'), text = request)
        ###Learning###

        post_event(intent_name, slot_values)
