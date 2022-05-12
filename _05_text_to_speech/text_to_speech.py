from decouple import config
from picotts import PicoTTS
import vlc
import subprocess

class TextToSpeech:
    
    def __init__(self):
        self.picotts = PicoTTS_(language = 'de-DE')
        self.wav_output_path = config('TTS_OUTPUT_PATH')
        self.dialog_manager_output_path = config('DIALOG_MANAGER_OUTPUT_PATH')
        self.vlc_audio_player = VLCAudio()

    def start(self):
        """
        generates wav file from given text then plays wav in a new process
        @param text: text to translate into audio
        """
        file = open(self.dialog_manager_output_path)
        for line in file:
            if "http" in line:
                self.vlc_audio_player.set_uri(line)
            else:
                self.vlc_audio_player.set_uri(self.wav_output_path)

                audio = self.picotts.engine.synth_wav(line)
                with open(self.wav_output_path, mode = 'bw') as wav:
                    wav.write(audio)

            self.vlc_audio_player.start_audio_player()

    def cleanup(self):
        """
        """
        subprocess.run(["rm", self.dialog_manager_output_path])


class PicoTTS_:

    def __init__(self, language):
        self.engine = PicoTTS()
        self.engine.voice = language

class VLCAudio:

    def __init__(self):
        self.vlc = vlc.Instance()
        self.audio_player = None

    def set_uri(self, uri):
        self.audio_player = self.vlc.media_player_new()
        self.audio_player.set_mrl(uri)

    def start_audio_player(self):
        self.audio_player.play()
