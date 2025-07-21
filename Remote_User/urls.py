from django.urls import path
from .views import *

urlpatterns=[
    path('$',home, name="home"),
    path('login/',login, name="login"),
    path('about/',about, name="about"),
    path('Technology/',Technology, name="Technology"),
    path('Research/',Research, name="Research"),
    path('Contacts/',Contacts, name="Contacts"),
    path('Register/',Register, name="Register"),
    path('Predict_Cardiac_Arrest_Type/',Predict_Cardiac_Arrest_Type, name="Predict_Cardiac_Arrest_Type"),
    path('ViewYourProfile/',ViewYourProfile, name="ViewYourProfile"),
    path('forget_password/',forget_password, name="forget_password"),
    path('Confirm_Password/',Confirm_Password, name="Confirm_Password"),
    path('Confirm_Email/',Confirm_Email, name="Confirm_Email"),
    path('resend_otp/',resend_otp, name="resend_otp"),
    path('Real_Time_Alerts/',Real_Time_Alerts, name="Real_Time_Alerts"),
]  