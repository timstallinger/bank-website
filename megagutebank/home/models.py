from pyexpat import model
from django.db import models

# Create your models here.

class Bank(models.Model):
    bilanz = models.FloatField()
    gewinn = models.FloatField()
    bic = models.CharField(max_length=11, primary_key=1)
    name = models.CharField(max_length=50)