from .import views
from django.urls import path

urlpatterns = [
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('registration/',views.user_registration,name='userregistration'),
    path('login/',views.logins,name='login')
]
