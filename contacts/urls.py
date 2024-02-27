from django.urls import path
from contacts.filters import *
from contacts.export import *
from contacts._import import *



urlpatterns = [
    path('get_all_contacts/', get_all_contacts, name='get-all_contacts'),
    path('get_contacts_by_type/', get_contacts_by_type, name='get-ontacts_by_type'),
    path('filter_contacts/', filter_contacts, name='filter-contacts'),
    path('export_organizations/', export_organizations, name='export-organizations'),
    path('export_contacts/', export_contacts, name='export-contacts'),
    path('import_org_data_from_pdf/', import_org_data_from_pdf, name='import-org_data_from_pdf'),
    path('import_contacts_data_from_pdf/', import_contacts_data_from_pdf, name='import-contacts_data_from_pdf'),
    path('import_organizations_from_csv/', import_organizations_from_csv, name='import-organizations_from_csv'),
    path('import_contacts_from_csv/', import_contacts_from_csv, name='import-contacts_from_csv'),
]
