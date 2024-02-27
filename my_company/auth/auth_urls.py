from django.urls import path
from my_company.views import *
from my_company.auth.auth import *

urlpatterns = [
    #Auth
    path('register/', register_MyInfo, name='register-MyInfo'),
    path('login/', login_view, name='login-MyInfo'),
    path('resend-verification/', resend_email_verification, name='resend-verification'),
    path('logout/', logout, name='logout-MyInfo'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:uid>/<str:token>/', reset_password, name='reset_password'),
    path('refresh_token/', refresh_token_view, name='refresh_token_view'),



    
    #email-verification 
    path('verify/<str:uidb64>/<str:token>/', email_verification, name='email-verification'),


]
