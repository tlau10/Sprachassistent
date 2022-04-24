from _04_dialog_manager.event import post_event
from voice_assistant_helper import read_json_file
from decouple import config

class DialogManager:

    def start(self):
        """
        reads json file from nlu, extracts data and calls execute method depending on found intent
        """
        intent = read_json_file(config('NLU_OUTPUT_PATH'))

        intent_name = intent['intent']['intentName']
        slots = intent['slots']

        slot_values = []
        for i in slots:
            slot_values.append(i['rawValue'])


        intent_to_event_listener= {
            'search_definition': 'wikipedia_search',
            'stop': 'stop',
            None : 'none'
        }
        # call execute method
        event = intent_to_event_listener[intent_name]
        post_event(event, slot_values)
