import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_DE
from decouple import config
from voice_assistant_helper import read_json_file

class NLU:

    def __init__(self):
        self.snips = Snips(config_type = CONFIG_DE)
        dataset = read_json_file(file_path = config('NLU_DATASET_PATH'))
        self.snips.engine.fit(dataset = dataset)

    def start(self, phrase):
        """
        start parsing text
        @param phrase: recognized phrase
        @return: intent with slots as json object
        """
        intent = self.snips.engine.parse(text = phrase)
        print(json.dumps(intent, indent = 2))
        return intent

class Snips:

    def __init__(self, config_type):
        self.engine = SnipsNLUEngine(config = config_type)
