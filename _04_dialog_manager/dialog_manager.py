from voice_assistant_helper import read_json_file
from decouple import config
import json
import wikipediaapi
import os
import subprocess

def default():
    print("No Skill matched")

def execute_wikipedia_skill(slot_values):
    wikipedia = wikipediaapi.Wikipedia('de')
    wikipedia_page = wikipedia.page(slot_values[0])
    page_summary = wikipedia_page.summary
    first_sentence = page_summary.split('.')[0]
    # TTS hängt sich an Satzzeichen und Umlauten auf -> evtl. anderes TTS auch mit mehr roboter artiger Sprache
    first_sentence = first_sentence.replace(',', '')
    print(first_sentence)

    run_tts(first_sentence)

def run_tts(text):
    output_file_path = config('DM_OUTPUT_PATH')
    model_path = config('TTS_MODEL_PATH')
    os.system('tts'+' --text ' + '"'+ text +'"' + ' --model_name ' + '"' + model_path + '"' + ' --model_name ' + '"' + model_path + '"')
    # TODO: os.system mit subprocess.run ersetzen um injections zu verhindern

def run_tts_2(text):
    pass


intent = read_json_file(config('NLU_OUTPUT_PATH'))

intent_name = intent['intent']['intentName']
slots = intent['slots']
slot_values = []

for i in slots:
    slot_values.append(i['rawValue'])


intent_to_skill_executor = {
    'search_definition': execute_wikipedia_skill,
    '': default
}
intent_to_skill_executor[intent_name](slot_values)