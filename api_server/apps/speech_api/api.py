"""
Взаимодействие api с различными пользователями
"""

from .models import SpeechApiModel
from rest_framework import viewsets, permissions
from .serializers import  SpeechApiSerializer, ResultApiSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

import scripts
from Speech2Text import combine
import os
import threading
import time
import shutil


def speech_to_txt(audio_file, model_choice, vocab):
    """
    Преобразование аудио речи в текст
    input: audio_file - аудио файл
           model_choice - выбранная модель
           vocab - вокабуляр
    """

    # сопоставление присланной модели с их ключами в базе данных
    model_choice = model_choice.split(' ')

    model = os.path.join('models', 'model_'+model_choice[0]+'_'+model_choice[1])
    audio = audio_file

    # получение вокабуляря в нужном формате
    new_vocab = scripts.delete_punctuation(vocab)

    #-------------start recognition and combining-----------------#
    print(f'\n your model {model}\n and audio_file {audio} \n')
    combine.main(audio, model, new_vocab)
    #-------------------------------------------------------------#
    pass


def get_result(session_id, encoded_data, extension, model, vocab):
    """
    получение результата обработки

    input: session_id - номер сессии
           extension - расширение исходного аудио
           model - используемая модель
           vocab - вокабуляр
    """

    print('GET RESULT')

    # получаем выгрузку из бд по всем запросам
    queryset = SpeechApiModel.objects.all()
    # фильтруем по номеру сессии
    session = get_object_or_404(queryset, pk=session_id)
    serializer = SpeechApiSerializer(session)

    # путь сохранения аудио файла
    name = os.path.join('media', 'audio')
    file = scripts.decode_file(encoded_data, name, session_id, extension)
    file_wav = scripts.convert_audio_to_mono_wav(file)

    #---------------------- Обработка словаря ---------------------------------#
    if len(vocab) != 0:

        # в начале получаем транскрипцию без словаря
        speech_to_txt(file_wav, model, '')

        name = file_wav.split('/')[1]
        txt_dir = f'txt_{name}'
        result = os.path.join(txt_dir, 'out.txt')
        with open(result, 'r') as file:
            result_txt = file.read()

        # удаляем промежуточную текстовую директорию
        shutil.rmtree(txt_dir)

        # создание вокабуляра из терминов и полученной транскрипции
        new_vocab = vocab + ' ' + result_txt
        # затем получаем транскрипцию со словарем
        if model.split(' ')[0] == 'ru':
            speech_to_txt(file_wav, 'ru simple', new_vocab)
        elif model.split(' ')[0] == 'en':
            speech_to_txt(file_wav, 'en simple', new_vocab)
    else:
        speech_to_txt(file_wav, model, vocab='')
    #---------------------- Конец обработки словаря  -----------------------#

    # получаем итоговый текст
    name = file_wav.split('/')[1]
    txt_dir = f'txt_{name}'
    result = os.path.join(txt_dir, 'out.txt')
    with open(result, 'r') as file:
        result_txt = file.read()

    # добавляем полученный результат в бд для дальнейшей выгрузки
    SpeechApiModel.objects.create(id=session_id, encoded_data="", ext="", result=result_txt)
    pass


class SpeechApiViewSet(viewsets.ModelViewSet):
    """
    Класс для взаимодействия api и пользователя
    """
    queryset = SpeechApiModel.objects.all()
    permission_classes = {
        permissions.AllowAny
    }
    serializer_class = SpeechApiSerializer

    def retrieve(self, request, pk=None):
        """
        Выгрузка для конкретной сессии
        input: pk - номер сессии
        """

        print("CALL SESSION REQUEST")

        queryset = SpeechApiModel.objects.all()
        session = get_object_or_404(queryset, pk=pk)
        serializer = ResultApiSerializer(session)
        content = {
	    'detail': 200,
            'session_id': serializer.data['id'],
            'result': serializer.data['result']
        }
        return Response(content)


    def list(self, request):
        """
        Выгрузка по всем запросам бд
        """
        print("CALL ALL GET REQUEST")

        queryset = SpeechApiModel.objects.all()
        serializer = ResultApiSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)


    def create(self, request):
        """
        Создание новой задачи для декдирования. Именно здесь обрабатвается приходящий запрос.
        """

        print("CREATE NEW RECORD")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            threading.Thread(target=get_result, args=(serializer.data['id'],serializer.data['encoded_data'], serializer.data['ext'], serializer.data['model'],serializer.data['vocab'])).start()
            content = {
                'detail': 200,
                'session_id': serializer.data['id'],
            }
            SpeechApiModel.objects.filter(id=serializer.data['id']).delete()
            return Response(content)

        return Response(serializer.data)
