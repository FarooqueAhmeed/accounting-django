from django.urls import path
from contacts.organization.views import *


urlpatterns = [
    path('manage_organization/', organization_api, name='organization-api'),
]




