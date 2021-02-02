from django.contrib import admin
from .models import Todo

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'extension', 'model', 'date')
    list_display_links = ('id', 'model',)
    search_fields = ('id', 'model')

admin.site.register(Todo, TodoAdmin)
