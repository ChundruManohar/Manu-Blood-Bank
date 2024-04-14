from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from datetime import datetime


# Create your views here.
def home(request):
    return JsonResponse({
        "message":"it is a home page",
        "status":"good",
    })
    
def about(request):
    return JsonResponse({
        "message":"it is a home page",
        "status":"good",
    })
@csrf_exempt
def user_registration(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": "Failed",
            "message": "Method Not Allowed"
        })

    try:
        data = json.loads(request.body)

        password     = (data.get('password'))
        if password == '' or password ==None:
            raise Exception("password cannot be empty")
        
        last_login   = datetime.now()

        is_superuser = data.get('is_superuser')

        username     =  data.get('username')
        if username == '' or username ==None:
            raise Exception("Username cannot be empty")
        
        first_name   = data.get('first_name')
        if first_name == '' or first_name ==None:
            raise Exception("first_name cannot be empty")
        
        last_name    = data.get('last_name')
        if last_name == '' or last_name ==None:
            raise Exception("last_name cannot be empty")
        
        email_id     = data.get('email')
        if email_id == '' or email_id ==None:
            raise Exception("email_id cannot be empty")
        
        is_staff     = data.get('is_staff')

        is_active    = data.get('is_active')

       # date_joined  = str(date.today())

        phone_number = data.get('phonenumber')

        bio    = data.get('bio')

        User_Registration = User.objects.create_user(
            password      =   password,
            last_login    =   last_login,
            is_superuser  =   is_superuser,
            username      =   username,
            first_name    =   first_name,
            last_name     =   last_name,
            email         =   email_id,
            is_staff      =   is_staff,
            is_active     =   is_active,
           # date_joined   =   date_joined,
            phone_number   =   phone_number,
            bio           =   bio,
            )

        return JsonResponse({
            "Status": "Success",
            "Message": f"User {username} Registered Successfully"
        })

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": f"Registration failed. {str(ex)}"
        })