from rest_framework import routers
from .api import SpeechApiViewSet
from django.urls import include
from . import views



router = routers.DefaultRouter()
router.register('api/speech_api',  SpeechApiViewSet, 'speech_api')

app_name = "speech_api"
urlpatterns = router.urls
