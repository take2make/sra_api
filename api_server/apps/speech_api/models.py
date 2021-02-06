"""
Описывается база данных для хранения, промежуточных результатов
"""

from django.db import models

class SpeechApiModel(models.Model):
    encoded_data = models.TextField()
    ext = models.CharField(max_length=300)

    # blank=True означает, что поле может быть пустым при заполнении бд
    model = models.CharField(max_length=300, blank=True)
    vocab = models.TextField(blank=True)
    result = models.TextField(blank=True)

    def __str__(self):
        return self.model
