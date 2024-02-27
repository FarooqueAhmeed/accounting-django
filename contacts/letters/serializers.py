from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.core.exceptions import ValidationError
from my_company.choices_LANGUAGES_COUNTRIES import *
from contacts.models import *

class LettersSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=True)
    your_signature = serializers.CharField(required=True, min_length=1, max_length=255)
    address = serializers.CharField(required=True, min_length=1, max_length=255)
    subject = serializers.CharField(required=True, min_length=1, max_length=255)
    country = serializers.ChoiceField(choices=COUNTRIES_CHOICES, required=True)
    text = serializers.CharField(required=True, min_length=1, max_length=1000)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='Draft')
    send_as = serializers.ChoiceField(choices=SEND_AS_CHOICES, default='Email')

    internal_contact_staff_name = serializers.SerializerMethodField()
    contact_receiver_first_name = serializers.SerializerMethodField()
    myinfo_first_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    contact_first_name = serializers.SerializerMethodField()

    class Meta:
        model = Letters
        fields = '__all__'


    def get_internal_contact_staff_name(self, obj):
        return obj.internal_contact_staff.name if obj.internal_contact_staff else None

    def get_contact_receiver_first_name(self, obj):
        return obj.contact_receiver.first_name if obj.contact_receiver else None

    def get_myinfo_first_name(self, obj):
        return obj.MyInfo.first_name if obj.MyInfo else None

    def get_organization_name(self, obj):
        return obj.organization.organization_name if obj.organization else None

    def get_contact_first_name(self, obj):
        return obj.contact.first_name if obj.contact else None

    def validate(self, data):
        # Additional validations
        if 'contact' in data and 'organization' in data and data['contact'] and data['organization']:
            raise ValidationError('Cannot specify both a contact and an organization.')

        # Validate each field individually
        for field in data.keys():
            # Skip validation for foreign key fields as you have custom logic for them
            if field in ['internal_contact_staff', 'contact_receiver', 'MyInfo', 'organization', 'contact']:
                continue
            
            # Get the field object from the model
            field_obj = self.Meta.model._meta.get_field(field)
            field_validators = field_obj.validators
            
            # Validate the field using the model field's validators
            for validator in field_validators:
                validator(data[field])

            # Check if the field is empty or exceeds the max length
            if not data[field] or (isinstance(data[field], str) and len(data[field]) > 255):
                raise ValidationError({field: 'This field cannot be empty or exceed 255 characters.'})

        return data


