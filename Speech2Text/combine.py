import Speech2Text.recognition as recognition
import os
import shutil
from threading import Thread


def open_file(file):
    """
    Открытие файла на считывание
    """

    with open(file, 'r') as f:
    	read_file = f.read()
    return read_file

def combine_txt(txt_dir):
    """
    Объединение фрагментов текста в окончательный

    Input: txt_dir - директория, где хранятся фрагменты для текущей сессии
    """

    # определяем количество фрагментов
    num_files = len(os.listdir(txt_dir))
    out_file = os.path.join(txt_dir, 'out.txt')

    with open(out_file, 'a') as f:
        for i in range(num_files):
            file = os.path.join(txt_dir, f'{i}.txt')
            txt = open_file(file)
            f.write(txt)

def main(audio_file, model_choice, DICT):
    """
    Запуск распознавания.

    input:
        На вход подается аудио файл преобразованный в формат mono wav: audio_file
        Выбранная модель: model_choice
        Опционально, словарь терминов: DICT
    """

    # получаем сессию и создаем директорию,
    # в которой будут хранится текстовые фрагменты
    session = audio_file.split('/')[1]
    txt_dir = f'txt_{session}'

    # запуск распознавания
    recognition.run(audio_file, model_choice, DICT)

    if os.path.isdir(txt_dir):
       print('COMBINING')
       # после того как фрагменты аудио распознаны
       # собираем их вместе (из текущей сессии)

       combine_txt(txt_dir)

       # удаление директории аудио файла
       os.remove(audio_file)
