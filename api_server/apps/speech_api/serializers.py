#  SpeechApi JSON

from rest_framework import serializers
from .models import SpeechApiModel


class SpeechApiSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SpeechApiModel
        fields = ('id', 'encoded_data', 'ext', 'model',)


class ResultApiSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SpeechApiModel
        fields = ('id', 'result',)
