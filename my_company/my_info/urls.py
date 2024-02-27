from django.urls import path
from my_company.my_info.views import *

urlpatterns = [
    path('update/', update_my_info, name='update-my-info'),
    path('userinfo/', get_user_info, name='get_user_info'),
    path('delete/', delete_my_info, name='delete_my_info'),



]

