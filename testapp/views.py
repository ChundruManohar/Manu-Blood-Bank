from django.shortcuts import render
import json
from django.http import JsonResponse

# Create your views here.
def home(request):
    return JsonResponse({
        "message":"it is a home page",
        "status":"good",
    })
    