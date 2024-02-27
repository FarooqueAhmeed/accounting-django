from rest_framework import serializers
from contacts.models import *
from django.core.validators import RegexValidator
from my_company.choices_LANGUAGES_COUNTRIES import *

class OrganizationSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(max_length=255,required=True,validators=[RegexValidator(regex=r'^[A-Za-z\s]+$',message="Organization name should contain only letters")])
    name_suffix = serializers.CharField(max_length=255,required=True,validators=[RegexValidator(regex=r'^[A-Za-z\s]+$',message="Name suffix should contain only letters.")])
    customer_number = serializers.CharField(max_length=255,required=True,validators=[RegexValidator(regex=r'^\d+$',message="Customer number should contain only digits.")])
    debtor_number = serializers.IntegerField(required=True,validators=[RegexValidator(regex=r'^\d+$',message="Debtor number should contain only digits.")])

    class Meta:
        model = Organization
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'