from django.db import models

# Create your models here.
# user contact model and user adddres details ok 
#user contact model
# name 
#email
# mobile Number 
# Dob 

# user address

class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile_Number = models.CharField(max_length=30)
    dob = models.DateTimeField()
    
class UserAdress(models.Model):
    name = models.ForeignKey(Users,on_delete=models.CASCADE)
    Address = models.CharField(max_length=100)
    