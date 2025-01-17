from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class ContactUs(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.full_name
    
class Subscribe(models.Model):
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email
