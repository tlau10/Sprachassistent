from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_DE
from decouple import config
from voice_assistant_helper import read_from_file, read_json_file, write_json_file

class NLU:

    def __init__(self):
        self.snips = Snips(config_type = CONFIG_DE)
        dataset = read_json_file(file_path = config('NLU_DATASET_PATH'))
        self.snips.engine.fit(dataset = dataset)

    def start(self):
        """
        start parsing text file, generates json file
        """
        stt_output = read_from_file(file_path = config('STT_OUTPUT_PATH'))
        result_json = self.snips.engine.parse(text = stt_output)

        write_json_file(file_path = config('NLU_OUTPUT_PATH'), json_object = result_json)

class Snips:

    def __init__(self, config_type):
        self.engine = SnipsNLUEngine(config = config_type)
