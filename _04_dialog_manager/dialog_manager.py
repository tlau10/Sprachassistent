from voice_assistant_helper import read_json_file
from _05_text_to_speech.text_to_speech import TextToSpeech
from decouple import config
import wikipediaapi
import subprocess
import multiprocessing
from playsound import playsound

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


        intent_to_skill_executor = {
            'search_definition': self.execute_wikipedia_skill,
            'stop': self.execute_stop_skill,
            None : self.execute_no_skill_matched
        }
        # call execute method
        intent_to_skill_executor[intent_name](slot_values)

    def execute_no_skill_matched(self, slot_values):
        """
        is executed if no skill was matched
        @param slot_values: empty list
        """
        self.run_tts("Ich kann dir leider nicht weiterhelfen!")

    def execute_wikipedia_skill(self, slot_values):
        """
        executes wikipedia skill by retrieving summary from wikipedia-api based on given search term
        @param slot_values: list of slot values
        """
        # no slot value recognized
        if len(slot_values) == 0:
            self.run_tts("Zu deinem Suchbegriff konnte leider nichts gefunden werden!")
            return

        search_term = slot_values[0]

        wikipedia = wikipediaapi.Wikipedia('de')
        wikipedia_page = wikipedia.page(search_term)

        # invalid slot value
        if not wikipedia_page.exists():
            response = "Zu dem Suchbegriff " + search_term + " existiert leider kein Wikipedia-Eintrag!"
            self.run_tts(response)
            return

        page_summary = wikipedia_page.summary

        first_sentence = page_summary.split('.')[0]
        self.run_tts(first_sentence)

    def execute_stop_skill(self, slot_values):
        print("voice assistant stopped...")
        self.run_tts("")

    def run_tts(self, text):
        """
        starts tts then plays generated .wav file
        @param text: text to say
        """
        tts = TextToSpeech()
        tts.text_to_wav(text)
        tts.play_audio()
