from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

#  Guest -- Movie --  Reservation

class Movie(models.Model):
    hall = models.CharField(max_length = 10)
    movie = models.CharField(max_length=20)
    # date = models.DateField()

class Guest(models.Model):
    name  = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11)

class Reservation(models.Model):
    # el related name bta3 el guest we use it 3shan lma n3ml query by use serilizers we use this name to get reservation bta3 el Guest da 
    # on_delete=models.CASCADE >>> 3shan lma n delete hna ysm3 hnak bardo
    guest = models.ForeignKey(Guest,related_name='reservation',on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='reservation',on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body =  models.TextField()


# code to add token automaticly for each user will be on system
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance) 
