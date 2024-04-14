from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User
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
    
def userregistration(request):
       return JsonResponse({
        "message":"it is a home page",
        "status":"good",
    })
    