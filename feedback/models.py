from django.db import models

# Create your models here.
class Feedback(models.Model):
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    isi = models.TextField()