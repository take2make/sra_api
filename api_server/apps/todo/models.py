from django.db import models
# Create your models here.

class Todo(models.Model):
    encoded_data = models.TextField()
    ext = models.CharField(max_length=300)
    model = models.CharField(max_length=300, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model
