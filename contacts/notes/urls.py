from django.urls import path
from contacts.notes.views import *


urlpatterns = [
    path('manage_notes/', manage_notes, name='manage-notes'),
]




