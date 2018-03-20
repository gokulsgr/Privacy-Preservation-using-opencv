from django.db import models

# Create your models here.



from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class posts(models.Model):
	fromuser = models.CharField(max_length=50,blank=True)
	touser = models.CharField(max_length=50, blank=True)
	message= models.TextField(max_length=100,blank=True)
	permission = models.BooleanField(default=False)
	image = models.ImageField()
	location= models.TextField(max_length=100,blank=True)
	typeof = models.CharField(max_length=50, blank=True)
	testimageloc=models.CharField(max_length=50, blank=True)

class imagesmodel(models.Model):
	image = models.ImageField()
	uname=models.CharField(max_length=50,blank=True)
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.uname+" "+str(self.image)