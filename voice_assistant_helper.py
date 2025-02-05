import struct
import wave
import json
import ast
import pyaudio

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

def read_from_file(file_path):
    """
    reads text from given file
    @param file path: relative path of file
    @return: text
    """
    with open(file_path, "r", encoding = "utf-8") as file:
        return file.read()

def read_from_file_by_line(file_path):
    """
    reads text from given file line by line
    @param file path: relative path of file
    @return: list of strings
    """
    with open(file_path, "r", encoding = "utf-8") as file:
        return file.readlines()

def write_to_file(file_path, text):
    """
    writes text to given file
    @param file_path: relative path of file
    @param text: string to write into file
    """
    with open(file_path, "w", encoding = "utf-8") as file:
        file.write(text)

def append_to_file(file_path, text):
    """
    appends text to given file
    @param file_path: relative path of file
    @param text: string to append to file
    """
    with open(file_path, "a", encoding = "utf-8") as file:
        file.write(text)

def read_json_file(file_path):
    """
    reads from given json file
    @param file path: relative path of file
    @return: dict object
    """
    with open(file_path, "r", encoding = "utf-8") as file:
        return json.load(file)

def write_json_file(file_path, json_object):
    """
    writes json object to given file
    @param file_path: relative path of file
    @param json_object: json object to write into file
    """
    json_object = json.dumps(json_object, indent = 2)
    print(json_object)
    write_to_file(file_path = file_path, text = json_object)

def convert_string_to_dict(string):
    """
    evaluates string then converts it to dict otherwise raises TypeError
    @param string: string to convert to dict
    @return: dict object
    """
    return ast.literal_eval(string)
