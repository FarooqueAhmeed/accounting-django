from django.urls import path
from contacts.letters.views import *


urlpatterns = [
    path('manage_letters/', manage_letters, name='manage-letters'),
]




