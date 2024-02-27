from django.urls import path
from .views import *

urlpatterns = [
    path('my_company_address/', my_company_address, name='my_company-address'),
    path('my_company_tax_info/', my_company_tax_info, name='my_company_tax'),
    path('manage_tags/', manage_tags, name='manage-tags'),
    path('my_company_contact_info/', my_company_contact_info, name='my_company_contact_info'),
    path('my_company_payment_info/', my_company_payment_info, name='my_company_payment-info'),
    path('my_company_logo/', my_company_logo, name='my_company_logo'),
    path('category_api/', category_api, name='category-api'),



]
