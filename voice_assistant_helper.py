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

def read_key_file(file_path):
    """
    reads key from given file
    @param file path: relative path of key file
    @return: key
    """
    file = open(file_path, "r")
    return file.read()

def record_audio(duration, sample_rate, frames):
    """
    records wav file from audio
    @param duration: amount of seconds to record
    """
    format = pyaudio.paInt16
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(
        rate = sample_rate,
        channels = 1,
        format = format,
        input = True,
        frames_per_buffer = frames
    )

    audio_frames = list()
    for i in range(0, int(sample_rate / frames * duration)):
        audio_data = audio_stream.read(frames)
        audio_frames.append(audio_data)

    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()

    wave_file = wave.open('in.wav', 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(b''.join(audio_frames))
    wave_file.close()

def write_to_file(file_path, text):
    """
    writes text to given file
    @param file_path: path to file
    @param text: string to write into file
    """
    file = open(file_path, "w")
    file.write(text)
    file.close()