from django.db import models

# Create your models here.
class User(models.Model):
  email = models.CharField(max_length= 30)
  password = models.CharField(max_length= 20)
  phone = models.CharField(max_length= 10)
  name = models.CharField(max_length= 40)

  def __str__(self):
    return self.name

class Restaurant(models.Model):
  name = models.CharField(max_length = 20)
  picture = models.URLField(max_length = 200, default='/delivery/images/default.jpg')
  cuisine = models.CharField(max_length = 200)
  address = models.CharField(max_length= 200, default= "No address provided")
  rating = models.FloatField()