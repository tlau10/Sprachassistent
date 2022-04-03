import pyaudio
import struct
from decouple import config
import wave

def get_next_audio_frame(sample_rate, frames):
    """
    returns audio frame from microphone
    @param sample_rate: number of frames per second
    @param frames: frames per buffer
    @return: next audio frame
    """

    audio = pyaudio.PyAudio()
    audio_stream = audio.open(
        rate = sample_rate,
        channels = 1,
        format = pyaudio.paInt16,
        input = True,
        frames_per_buffer = frames
    )

    audio_frame = audio_stream.read(frames)

    # convert to short datatype
    audio_frame = struct.unpack_from("h" * frames, audio_frame)

    audio.close(audio_stream)
    return audio_frame

def play_notification_sound(file_path):
    """
    play sound from given file
    @param file_path: relative path of wav file
    """
    file = wave.open(file_path, 'rb')

    audio = pyaudio.PyAudio()
    audio_output = audio.open(
        format = pyaudio.paInt16,
        channels = file.getnchannels(),
        rate = file.getframerate(),
        output = True)

    chunk_size = 1024
    audio_data = file.readframes(chunk_size)
    while len(audio_data) > 0:
        audio_output.write(audio_data)
        audio_data = file.readframes(chunk_size)

    audio.close(audio_output)
