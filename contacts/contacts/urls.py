from django.urls import path
from contacts.contacts.views import *


urlpatterns = [
    path('manage_contacts/', contact_api, name='contact-api'),
]




