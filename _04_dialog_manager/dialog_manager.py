from voice_assistant_helper import read_json_file
from decouple import config
import wikipediaapi
import subprocess

def default():
    print("No Skill matched")

def execute_wikipedia_skill(slot_values):
    wikipedia = wikipediaapi.Wikipedia('de')
    wikipedia_page = wikipedia.page(slot_values[0])
    page_summary = wikipedia_page.summary
    first_sentence = page_summary.split('.')[0]
    first_sentence = '"' + first_sentence + '"'

    print(first_sentence)

    run_tts(first_sentence)

def run_tts(text):
    output_file_path = config('TTS_OUTPUT_PATH')
    subprocess.call(['pico2wave', '-l', 'de-DE', '-w', output_file_path, text])
    subprocess.call(['aplay', output_file_path])


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