from _04_dialog_manager.event import post_event
from _04_dialog_manager.observer import setup_event_handlers
from voice_assistant_helper import read_json_file
from decouple import config

class DialogManager:

    def __init__(self):
        # setup all event handlers
        setup_event_handlers()

    def start(self):
        """
        reads json file from nlu, extracts data and calls execute method depending on found intent
        """
        intent = read_json_file(config('NLU_OUTPUT_PATH'))

        intent_name = intent['intent']['intentName']
        slots = intent['slots']

        slot_values = []
        for slot in slots:
            slot_values.append(slot['rawValue'])

        # no intent matched
        if not intent_name:
            post_event("none", slot_values)

        post_event(intent_name, slot_values)
