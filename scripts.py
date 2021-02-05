import base64
import os
import re

def delete_punctuation(txt_file):
	without_punctuation = re.sub(r'[^\w\s]','',txt_file)
	without_numbers = re.sub(r'[0-9]+', '', without_punctuation)
	return without_numbers.rstrip('\n')

def decode_file(encoded_data, name, session, extension):
    file_res = f'{name}_{session}.{extension}'
    with open(file_res, "wb") as file:
        decoded_data = base64.b64decode(encoded_data)
        file.write(decoded_data)
    return file_res

def convert_audio_to_mono_wav(decoded_data):
    os.system(f'ffmpeg -i {decoded_data} -acodec pcm_s16le -ac 1 -ar 8000 {decoded_data}.wav')
    os.remove(decoded_data)
    return f'{decoded_data}.wav'
