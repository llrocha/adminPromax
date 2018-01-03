from django.db import models

# Create your models here.
class Config(models.Model):
        key = models.CharField(max_length=32)
        value = models.CharField(max_length=256)
        def __str__(self):
                return self.key + ' = ' + self.value