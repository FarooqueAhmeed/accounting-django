from django.urls import path
from .views import *

urlpatterns = [
    path('login_staff/', login_staff, name='login-staff'),

]
