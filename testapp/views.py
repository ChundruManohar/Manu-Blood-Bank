from django.shortcuts import render
import json
from rest_framework.response import Response
from django.http import JsonResponse
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives,send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


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
        
        last_login   = timezone.now()

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
        
        emailId     = data.get('email')
        if emailId == '' or emailId ==None:
            raise Exception("emailId cannot be empty")
        
        is_staff     = data.get('is_staff')

        is_active    = data.get('is_active')

        #date_joined  = str(date.today())

        phone_number = data.get('phonenumber')

        bio    = data.get('bio')

        User_Registration = User.objects.create_user(
            password      =   password,
            last_login    =   last_login,
            is_superuser  =   is_superuser,
            username      =   username,
            first_name    =   first_name,
            last_name     =   last_name,
            email         =   emailId,
            is_staff      =   is_staff,
            is_active     =   is_active,
           # date_joined   =   date_joined,
            phone_number   =   phone_number,
            bio           =   bio,
            )
        
        
        send_mail(
            "congrations",
            "you are register sucessfully",
            settings.EMAIL_HOST_USER,
            [emailId,"manoharchundru@gmail.com"],
            fail_silently=False
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
        
        
        
@csrf_exempt       
def logins(request):
    if request.method != "POST":
        return JsonResponse({
            "status":"failed",
            "message":"method not allowed"    
        })
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "failed", "message": "Invalid JSON"}, status=400)
        
    userName = data.get("username")
    passWord = data.get("password")
    if userName == "" or userName == None or passWord =="" or passWord ==None:
            raise Exception("Either username or password cannot be empty")
    else:
        user = authenticate(request, username=userName, password=passWord)
        if user is not None:
            refresh =RefreshToken.for_user(user)
            return JsonResponse({
                    "refresh_token": str(refresh),
                    "acess_token":str(refresh.access_token)
            })


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])  
def updateuser(request):
    try:
        user = User.objects.filter(pk = request.user.id).exists()
        if user == False:
            raise Exception("user does not exist")
        user_obj = User.objects.get(pk = request.user.id)
        data = request.data
        user_obj.first_name=data.get("first_name")
        user_obj.last_name=data.get("last_name")
        user_obj.email=data.get("email")
        user_obj.phone_number=data.get("phonenumber")
        user_obj.bio=data.get("bio")
        user_obj.save()
        return JsonResponse({
            "status":"updated user",
            "message":"sucessfully"
        })
        
    except Exception as ex:
        return JsonResponse({
            "status":"failed",
            "message": str(ex)
        })
