import base64
import os
import re

"""
Набор необходимых скриптов
"""


def delete_punctuation(txt_file):
	"""
	Удаление пунктуации и приведения текста к виду, необходимому для использования в качестве словаря

	input: txt_file - подается текстовый файл

	output: текст без пунктуации в нижнем регистре
	"""
	
	without_punctuation = re.sub(r'[^\w\s]','',txt_file)
	without_numbers = re.sub(r'[0-9]+', '', without_punctuation)
	return without_numbers.rstrip('\n').lower()


def decode_file(encoded_data, name, session, extension):
	"""
	Поскольку данные на сервер присылаются в декодированном виде (это необходимо для их отправки на сервер),
	на стороне сайта необходимо их обратно декодировать

	input: encoded_data - декодированные данные
		   name - названия файла, в который осуществляется сохранение
		   session - номер сессии, необходимо для одновременной работы многих пользователей на сайте и api
		   extension - расширение декодированного файла
	"""

    file_res = f'{name}_{session}.{extension}'
    with open(file_res, "wb") as file:
        decoded_data = base64.b64decode(encoded_data)
        file.write(decoded_data)
    return file_res


def convert_audio_to_mono_wav(decoded_data):
	"""
	Поскольку vosk api принимает аудио определенного формата mono wav, а пользователь отправляет данные
	в другим расширением, например mp3, mp4a, mp4 etc, необходимо преобразовать их к нужному формату.

	input: decoded_data - аудио данные в исходном расширении

	output: аудио данные в формате mono wav
	"""

    os.system(f'ffmpeg -i {decoded_data} -acodec pcm_s16le -ac 1 -ar 8000 {decoded_data}.wav')
    os.remove(decoded_data)
    return f'{decoded_data}.wav'
