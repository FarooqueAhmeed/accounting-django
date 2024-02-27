from django.urls import path
from .views import manage_tasks

urlpatterns = [
    path('manage_tasks/', manage_tasks, name='manage-tasks'),
]
