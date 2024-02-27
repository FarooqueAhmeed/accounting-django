from rest_framework import serializers
from contacts.models import *
from my_company.choices_LANGUAGES_COUNTRIES import *
from django.contrib.auth.hashers import make_password


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

    email = serializers.EmailField(required=True,error_messages={'required': 'Email is required.','blank': 'Email cannot be be blank.','invalid': 'Invalid email format.','unique': 'This email address is already associated with an existing Staff account.'})
    user_type = serializers.ChoiceField(required=True,choices=[user_type[0] for user_type in Staff.MyInfo_TYPES],error_messages={'required': 'User type is required.','invalid_choice': 'Invalid user type.'})
    salutation = serializers.ChoiceField(required=True,choices=[salutation[0] for salutation in Staff.SALUTATION_CHOICES],error_messages={'required': 'Salutation is required.','invalid_choice': 'Invalid salutation.'})
    language = serializers.ChoiceField(required=True,choices=[language[0] for language in LANGUAGES_CHOICES],error_messages={'required': 'Language is required.','invalid_choice': 'Invalid language.'})
    password = serializers.CharField(required=True,error_messages={'required': 'Password is required.'}) 
    
    def create(self, validated_data):
        # Hash the password before saving it
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        return super(StaffSerializer, self).create(validated_data)
    
    def validate_user_type(self, value):
        # Validate the user_type field
        valid_user_types = [user_type[0] for user_type in Staff.MyInfo_TYPES]
        if value not in valid_user_types:
            raise serializers.ValidationError("Invalid user type.")
        return value

    def validate_salutation(self, value):
        # Validate the salutation field
        valid_salutations = [salutation[0] for salutation in Staff.SALUTATION_CHOICES]
        if value not in valid_salutations:
            raise serializers.ValidationError("Invalid salutation.")
        return value

    def validate_language(self, value):
        # Validate the language field
        valid_languages = [language[0] for language in LANGUAGES_CHOICES]
        if value not in valid_languages:
            raise serializers.ValidationError("Invalid language.")
        return value
    
    def validate_password(self, value):
        # Validate the password field according to your criteria
        # Add your password validation logic here
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value