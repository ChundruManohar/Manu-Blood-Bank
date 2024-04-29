from .import views
from django.urls import path

urlpatterns = [
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('registration/',views.user_registration,name='userregistration'),
    path('login/',views.logins,name='login'),
    path('updateuser/',views.updateuser,name='updateuser'), 
    path('otpsender/',views.opt_Sender,name='otpSender'),
    path('confirm_otp/',views.confirm_otp,name='confirm_otp'),
    path('reset_PWD/',views.password_reset,name='password_reset'),
    path('create_campin/',views.created_campin,name='created_campin'),
    path('campin_list/',views.campin_list,name='campinlist'),
    path('extendsCampainEnddate/',views.extendCampainEnddate,name='CamppinEnddate'),
]
