import os
import ffmpeg
from threading import Thread
import time
import shutil
from vosk import Model, KaldiRecognizer
import wave
import json


def get_length_audio(audio):
	"""
	Получение продолжительности аудио фрагмента

	input: audio - исходное аудио

	output: length - длина аудио фрагмента в секундах
	"""

	length = ffmpeg.probe(audio)['format']['duration']
	return float(length)


def cutting_original_audio(audio, cut_dir, split_size=60*3):
	"""
	Нарезка исходного аудио на фрагменты в cut_dir

	input: audio - исходного аудио
		   cut_dir - директория для сохранения нарезаемых фрагментов
		   split_size - размер нарезки (по умолчанию 3 минуты)

    output: new_audio_files - нарезанные аудио фрагменты
	"""

	# продолжительность аудио фрагмента
	length = get_length_audio(audio)

	# определение количества фрагментов
	nums = round(length/split_size)

	new_audio_file = []
	for i in range(nums):
		# создание файлов и нарезка
		# !!! на компьютере должна быть установлена ffmpeg !!!
		new_audio_file.append(os.path.join(cut_dir, f'cut-{i}.wav'))
		os.system(f'ffmpeg -ss {i*split_size} -t {split_size} -i {audio} -ab 256k {new_audio_file[i]}')

	return new_audio_file


def read_wave(wf, rec):
	"""
	Считывагте аудио фрагмента.
	input: rec - используемый конвертер
		   wf - поток аудио

    output: ans - текстовая транскрипция аудио
	"""
	ans = ""
	while True:
		# считываем по конкретным размерам
	    data = wf.readframes(10000)
	    if len(data) == 0:
	        break
	    if rec.AcceptWaveform(data):
			# если предложение заканчивается, записываем его
			# в результат
	        json_dump = json.loads(rec.Result())
	        tmp = json_dump['text']
	        tmp = tmp.capitalize()
	        ans += tmp
	        ans += '. '

	return ans


def save_file(result, file):
	"""
	Сохранение результата в файл
	"""
	with open(file,"w") as f:
	    f.write(result)


class SpeechToText(Thread):
    def __init__(self, number, audio_name, txt_dir):
        """
		Инициализация потока. Конкретный поток обрабатывает
		аудио файл с именем audio_name

		input: number - номер фрагмента (совпадает с номером запускаемого потока)
			   audio_name - фрагмент аудио
		"""
        Thread.__init__(self)
        self.number = number
        self.audio_name = audio_name
        self.txt_dir = txt_dir

    def run(self):
        """
		Запуск потока. Запуск конвертации фрагмента
		"""
        print(f'start reading {self.audio_name}')
        start_time = time.time()

        wf = wave.open(self.audio_name, 'rb')

		# если пользователь подает словарь, то мы используем его для
		# конвертации аудио речи в текст
        global DICT
        if len(DICT)!= 0:
        	rec = KaldiRecognizer(model, wf.getframerate(), f'["{DICT}"]')
        else:
            rec = KaldiRecognizer(model, wf.getframerate())

		# считывание аудио
        audio_rec = read_wave(wf, rec)

		# сохранение записи audio_rec под нужным именем в директории
		# self.txt_dir.
		# !!! для каждой новой сессии, self.txt_dir разное !!!
        txt_file = os.path.join(self.txt_dir, f'{self.number}.txt')
        result = '{}'.format(audio_rec)
        save_file(result, txt_file)

        os.remove(self.audio_name)
        print("--- {} seconds ---".format(time.time() - start_time))
        print(f"/nЗакончил считывание {self.audio_name}/n")


def main(audio_files, txt_dir):
	"""
	Создание потоков для обработки фрагментов аудио

	input: audio_files - имена нарезанных аудио файлов
		   txt_dir - путь сохрания конвертации
	"""

	threads = []
	for num, audio_name in enumerate(audio_files):
		threads.append(SpeechToText(num, audio_name, txt_dir))
		threads[num].start()
	return threads


def run(audio_file, model_choice, vocab):
	"""
	Запуск распознавания аудио речи.

	input: audio_file в нужном формате (mono wav)
	 	   model_choice - выбранная модель
		   vocab - вокабуляр с терминами

	"""

	if not os.path.exists(model_choice):
		print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
		exit (1)

	global DICT
	DICT = vocab
	global model

	# Инициализация модели
	model = Model(model_choice)

	# получение сессии работы
	name = audio_file.split('/')[1]
	cut_dir = f'cut_dir_{name}'
	txt_dir = f'txt_{name}'

	if os.path.isdir(cut_dir):
		shutil.rmtree(cut_dir)
	if os.path.isdir(txt_dir):
		shutil.rmtree(txt_dir)
	os.mkdir(cut_dir)
	os.mkdir(txt_dir)

	# режем исходное аудио на фрагменты, и запускаем их обработку
	# в отдельных потоках
	new_audio_files = cutting_original_audio(audio_file, cut_dir)

	# создание потоков
	threads = main(new_audio_files, txt_dir)
	for thr in threads:
		# ожидаем завершения всех потоков
		thr.join()
	shutil.rmtree(cut_dir)
