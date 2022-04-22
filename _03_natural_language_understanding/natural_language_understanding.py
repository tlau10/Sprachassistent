from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_DE
from voice_assistant_helper import read_from_file, read_json_file, write_to_file
from decouple import config
import json

class NLU:

    def __init__(self):
        self.snips = Snips(config = CONFIG_DE)
        dataset = read_json_file(config('NLU_DATASET_PATH'))
        self.snips.engine.fit(dataset)

    def start(self):
        """
        start parsing text file, generates json file
        """
        stt_output = read_from_file(config('STT_OUTPUT_PATH'))
        result_json = self.snips.engine.parse(stt_output)
        result_json = json.dumps(result_json, indent = 2)

        print(result_json)
        write_to_file(file_path = config('NLU_OUTPUT_PATH'), text = result_json)

class Snips:

    def __init__(self, config):
        self.engine = SnipsNLUEngine(config = config)