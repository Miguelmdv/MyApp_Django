from django.db import models

# Create your models here.
class Proyect(models.Model):
    name = models.CharField(max_length=200)
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    proyect = models.ForeignKey(Proyect, on_delete=models.CASCADE)