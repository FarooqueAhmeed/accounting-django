from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from contacts.models import *


class TaskSerializer(serializers.ModelSerializer):


    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_description(self, value):
        if not value:
            raise ValidationError('The description field cannot be empty.')
        return value

    def validate_days(self, value):
        if value is None:
            raise ValidationError('The days field is required.')
        return value

    def validate_due_date(self, value):
        if value is None:
            raise ValidationError('The due date field is required.')
        return value

    def validate_type_of_task(self, value):
        if not value:
            raise ValidationError('The type of task field cannot be empty.')
        return value


    def validate(self, data):
        # Additional validations
        organization = data.get('organization')
        contact = data.get('contact')
        
        if organization and contact:
            raise ValidationError('Cannot specify both a contact and an organization.')

        # Custom validation logic if necessary
        if organization is None and contact is None:
            raise ValidationError('At least one of organization or contact must be set.')

        return data

