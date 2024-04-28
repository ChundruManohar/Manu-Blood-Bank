from django.shortcuts import render
import json
from rest_framework.response import Response
from django.http import JsonResponse
from .models import User,Campagin,Contribution
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives,send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum,Max,Min,aggregates
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime,date

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

@csrf_exempt
def opt_Sender(request):
    emailId = (json.loads(request.body))['email'] 
    try:
        user = User.objects.get(email = emailId)
    except User.DoesNotExist():
        return JsonResponse({
            "status":"failed",
            "message":"user not exist",
        })
        
        
    otp = get_random_string(length=4,allowed_chars=("1234567890"))
    cache.set(emailId,otp,timeout=300)
    
    subject="Password reset otp"
    from_email = settings.EMAIL_HOST_USER 
    recepient_list = [emailId,'manoharchundru@gmail.com','manohar1231997@outlookoutlook.com']
    html_msg =  render_to_string('otp_send.html',{"Otp":otp})
    email = EmailMultiAlternatives(subject,'',from_email,recepient_list)
    email.attach_alternative(html_msg,"text/html")
    email.send()
    return JsonResponse({
        "status":"sucesss",
        "meessage": f"email sent the user"
    })
    
@api_view(["POST"])
def confirm_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    cached_Otp = cache.get(email)
    if cached_Otp is None or cached_Otp != otp:
        return JsonResponse({"message":"Invalid OTP"})
    return JsonResponse({"message":"veryfied otp sucessfully"})
    
@api_view(["POST"])
def password_reset(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    
    if password != confirm_password:
        return JsonResponse({"meassage":"password not matched"})
    
    catched_otp = cache.get(email)
    
    if catched_otp is None:
        return JsonResponse({"message":"otp expered"})
    
    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist():
        return JsonResponse({
            "message":" user not found",
        })
    user.set_password(password)
    user.save()
    
    cache.delete(email)
    
    subject= "PASSWORD SAVED"
    from_email = settings.EMAIL_HOST_USER 
    recepient_list =[email]
    
    html_message = render_to_string('pwd_reset.html',{"password":password})
    
    try:
        email = EmailMultiAlternatives(subject,'',from_email,recepient_list)
        email.attach_alternative(html_message,"text/html")
        email.send()
        return JsonResponse({"message":"Password reset sucessfully"})
    except:
        return JsonResponse({"message":"passwod reset sucessfully but send it fail in email"})
    
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])

def created_campin(request):
    data = json.loads(request.body)
    
    title = data.get('title')
    description = data.get('description')
    funding_goal = data.get('funding_goal')
    campin_End_date = data.get('campin_end_date')
    if not title or not description or not funding_goal or not campin_End_date:
        return JsonResponse({
            "status":"failed",
            "message":"data is incomplete"
        })
        
    campin_Start_date = str(date.today())
    
    Campin_obj = Campagin.objects.create(
        title=title,
        description =description,
        funding_goal=funding_goal,
        campin_end_date = campin_End_date,
        campin_Start_date = campin_Start_date,
        owner = request.user
    )
    Campin_obj.save()
    
    return JsonResponse({
        "status":"sucessfully",
        "message":"ok created campain sucessfully"
    })