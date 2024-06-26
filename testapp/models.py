from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=models.BigIntegerField(null=True,blank=True)
    bio = models.TextField(max_length=500)
    
class Campagin(models.Model):
    title =models.CharField(max_length=100)
    description = models.TextField()
    funding_goal = models.IntegerField()
    campin_Start_date = models.DateField()
    campin_end_date = models.DateField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    
class Contribution(models.Model):
    amount = models.IntegerField()
    project = models.ForeignKey(Campagin,on_delete=models.CASCADE)
    contributer = models.ForeignKey(User,on_delete=models.CASCADE)
    