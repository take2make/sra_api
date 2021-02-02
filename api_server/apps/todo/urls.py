from rest_framework import routers
from .api import TodoViewSet
from django.urls import include
from . import views



router = routers.DefaultRouter()
router.register('api/todo', TodoViewSet, 'todo')

app_name = "todo"
urlpatterns = router.urls
