#  SpeechApi JSON

from rest_framework import serializers
from .models import SpeechApiModel


class SpeechApiSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SpeechApiModel
        fields = ('id', 'encoded_data', 'ext', 'model','vocab',)


class ResultApiSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SpeechApiModel
        fields = ('id', 'result',)
