from django.contrib import admin
from .models import SpeechApiModel

# Адимнка для апи (Опционально)
class SpeechApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'ext', 'model')
    list_display_links = ('id', 'model',)
    search_fields = ('id', 'model')

admin.site.register(SpeechApiModel, SpeechApiAdmin)
