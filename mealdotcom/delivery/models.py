from django.db import models

# Create your models here.
class User(models.Model):
  email = models.CharField(max_length= 30)
  password = models.CharField(max_length= 20)
  phone = models.CharField(max_length= 10)
  name = models.CharField(max_length= 40)

def __str__(self):
    return self.name
