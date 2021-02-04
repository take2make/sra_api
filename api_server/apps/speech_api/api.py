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

def speech_to_txt(audio_file, model_choice):
    model_choice = model_choice.split(' ')

    model = os.path.join('models', 'model_'+model_choice[0]+'_'+model_choice[1])
    audio = audio_file

    #-------------start recognition and combining-----------------#
    print(f'\n your model {model}\n and audio_file {audio} \n')
    combine.main(audio, model)
    #-------------------------------------------------------------#
    pass


def get_result(session_id, encoded_data, extension, model):
    print('GET RESULT')

    queryset = SpeechApiModel.objects.all()
    session = get_object_or_404(queryset, pk=session_id)
    serializer = SpeechApiSerializer(session)
    print(serializer.data)

    name = os.path.join('media', 'audio')
    file = scripts.decode_file(encoded_data, name, session_id, extension)
    file_wav = scripts.convert_audio_to_mono_wav(file)

    speech_to_txt(file_wav, model)

    name = file_wav.split('/')[1]
    result = os.path.join(f'txt_{name}', 'out.txt')
    with open(result, 'r') as file:
        result_txt = file.read()
    shutil.rmtree(txt_dir)
    SpeechApiModel.objects.create(id=session_id, encoded_data="", ext="", result=result_txt)
    pass


class SpeechApiViewSet(viewsets.ModelViewSet):
    queryset = SpeechApiModel.objects.all()
    permission_classes = {
        permissions.AllowAny
    }
    serializer_class = SpeechApiSerializer

    def retrieve(self, request, pk=None):
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
        print("CALL ALL GET REQUEST")

        queryset = SpeechApiModel.objects.all()
        serializer = ResultApiSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)


    def create(self, request):
        print("CREATE NEW RECORD")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            threading.Thread(target=get_result, args=(serializer.data['id'],serializer.data['encoded_data'], serializer.data['ext'], serializer.data['model'],)).start()
            content = {
                'detail': 200,
                'session_id': serializer.data['id'],
            }
            SpeechApiModel.objects.filter(id=serializer.data['id']).delete()
            return Response(content)

        return Response(content)
