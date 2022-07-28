from decouple import config
from picotts import PicoTTS
import vlc
from voice_assistant_helper import read_from_file

class TextToSpeech:

    def __init__(self):
        self.picotts = Pico(language = 'de-DE')
        self.wav_output_path = config('TTS_OUTPUT_PATH')
        self.vlc_audio_player = VLCAudio()

    def start(self, response):
        """
        reads output file from dialog manager and either generates wav file or sets up http stream,
        then plays audio using vlc
        """
        print(response)
        if not response:
            self.vlc_audio_player.stop_audio_player()
            return

        # set uri depending on line
        if "http" in response:
            self.vlc_audio_player.stop_audio_player()
            self.vlc_audio_player.set_uri(uri = response)
        else:
            self.vlc_audio_player.stop_audio_player()
            self.vlc_audio_player.set_uri(uri = self.wav_output_path)

            # generate wav file
            audio = self.picotts.engine.synth_wav(txt = response)
            with open(self.wav_output_path, mode = 'bw') as wav:
                wav.write(audio)

        # starts the audio player
        self.vlc_audio_player.start_audio_player()

class Pico:

    def __init__(self, language):
        self.engine = PicoTTS()
        self.engine.voice = language

class VLCAudio:

    def __init__(self):
        self.vlc = vlc.Instance()
        self.audio_player = None

    def set_uri(self, uri):
        """
        starts new media player then sets uri
        @param uri: path to wav file or url of stream
        """
        self.audio_player = self.vlc.media_player_new()
        self.audio_player.set_mrl(uri)

    def start_audio_player(self):
        """
        starts the audio player
        """
        if self.audio_player:
            self.audio_player.play()

    def stop_audio_player(self):
        """
        stops the audio player
        """
        if self.audio_player:
            self.audio_player.stop()
