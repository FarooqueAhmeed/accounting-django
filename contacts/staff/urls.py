from django.urls import path
from contacts.staff.views import *




urlpatterns = [
    path('manage_staff/', manage_staff, name='manage-staff'),

]
