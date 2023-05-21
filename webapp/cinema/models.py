from django.db import models

# Create your models here.

class NewVideo(models.Model):
    name = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    image = models.ImageField()
    url = models.URLField()