from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_DE
from voice_assistant_helper import read_key_file, read_json_file, write_to_file
from decouple import config
import json

class NLU:
    def __init__(self):
        self.snips = Snips(config = CONFIG_DE)

    def train(self):
        dataset = read_json_file(config('NLU_DATASET_PATH'))
        self.snips.engine.fit(dataset)

    def parse(self):
        stt_input = read_key_file(config('STT_FILE_PATH'))
        result_json = self.snips.engine.parse(stt_input)
        result_json = json.dumps(result_json, indent = 2)

        print(result_json)
        write_to_file(file_path = config('NLU_OUTPUT_PATH'), text = result_json)

class Snips:
    def __init__(self, config):
        self.engine = SnipsNLUEngine(config = config)
