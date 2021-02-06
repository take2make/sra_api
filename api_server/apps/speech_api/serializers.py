"""
Описывается json структура, отправляемых файлов
"""

from rest_framework import serializers
from .models import SpeechApiModel



class SpeechApiSerializer(serializers.ModelSerializer):
    """
    json структура отправляемых файлов на сервер

    id - номер рабочей сессии (для каждого нового запуска уникальное значение)
    encoded_data - закодированные данные
    ext - расширение
    model - модель (на данный момент доступны 4 (ru simple, ru hard, en_simple, en_hard))
    vocab - вокабуляр терминов

    Для отправки необходимо заполнять json следующим образом:
    {'encoded_data': encoded_data, 'ext': ext, 'model': model, 'vocab': vocab}

    """
    class Meta:
        model =  SpeechApiModel
        fields = ('id', 'encoded_data', 'ext', 'model','vocab',)


class ResultApiSerializer(serializers.ModelSerializer):
    """
    json структура присыламых серверов результатов конвертации.

    id - номер рабочей сессии
    result - результирующий текст
    """
    class Meta:
        model =  SpeechApiModel
        fields = ('id', 'result',)
