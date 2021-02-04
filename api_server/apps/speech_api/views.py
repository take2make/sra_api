from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import SpeechApiModel
from .serializers import SpeechApiSerializer
from rest_framework.response import Response


# Create your views here.
class SpeechApiViewSet(APIView):

    parser_classes = (FormParser, MultiPartParser)

    def get(self, request, format=None):

        data = SpeechApiModel.objects.all()

        serializer = SpeechApiSerializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

       serializer = SpeechApiSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
