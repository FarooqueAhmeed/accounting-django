from rest_framework import serializers
from contacts.models import *
from django.core.validators import RegexValidator
from my_company.choices_LANGUAGES_COUNTRIES import *



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        extra_kwargs = {
            'salutation': {'required': True, 'error_messages': {'required': 'Salutation is required.'}},
            'title': {'required': True, 'error_messages': {'required': 'Title is required.'}},
            'first_name': {'required': True, 'error_messages': {'required': 'First Name is required.'}},
            'last_name': {'required': True, 'error_messages': {'required': 'Last Name is required.'}},
            'legal_name': {'required': True, 'error_messages': {'required': 'Legal Name is required.'}},
            'customer_number': {'required': True, 'error_messages': {'required': 'Customer Number is required.'}},
            'line_item': {'required': True, 'error_messages': {'required': 'Line Item is required.'}},
            'debtor_number': {'required': True, 'error_messages': {'required': 'Debtor Number is required.'}},
            'contact_type': {'required': False},  
            'organization': {'required': False},  
            'MyInfo': {'required': False},  
        }

    def validate_debtor_number(self, value):
        """
        Validate that debtor_number is a positive integer.
        """
        if value < 0:
            raise serializers.ValidationError("Debtor number must be a positive integer.")
        return value

    def validate_customer_number(self, value):
        """
        Validate that customer_number is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Customer number cannot be empty.")
        return value

    def validate_first_name(self, value):
        """
        Validate that first_name contains only letters or spaces.
        """
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("First name should contain only letters and spaces.")
        return value

    def validate_last_name(self, value):
        """
        Validate that last_name contains only letters or spaces.
        """
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Last name should contain only letters and spaces.")
        return value

    def validate_legal_name(self, value):
        """
        Validate that legal_name contains only letters or spaces.
        """
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Legal name should contain only letters and spaces.")
        return value

    def validate_salutation(self, value):
        """
        Validate that salutation is one of the predefined choices.
        """
        if value not in dict(Contact.SALUTATION_CHOICES).keys():
            raise serializers.ValidationError("Invalid salutation value.")
        return value





