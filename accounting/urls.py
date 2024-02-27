from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from django.urls import re_path



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('my_company/', include('my_company.urls')),
    path('auth/', include('my_company.auth.auth_urls')),
    path('myinfo/', include('my_company.my_info.urls')),
    path('mycomapny/', include('my_company.company.urls')),
    path('organization/', include('contacts.organization.urls')),
    path('contacts/', include('contacts.contacts.urls')),
    path('all_contacts/', include('contacts.urls')),
    path('notes/', include('contacts.notes.urls')),
    path('staff/', include('contacts.staff.urls')),
    path('staff_auth/', include('contacts.staff.auth.urls')),
    path('letters/', include('contacts.letters.urls')),
    path('tasks/', include('contacts.tasks.urls')),




]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
