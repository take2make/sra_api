from django.db import models
# Create your models here.

class SpeechApiModel(models.Model):
    encoded_data = models.TextField()
    ext = models.CharField(max_length=300)
    model = models.CharField(max_length=300, blank=True)
    vocab = models.TextField(blank=True)
    result = models.TextField(blank=True)

    def __str__(self):
        return self.model
