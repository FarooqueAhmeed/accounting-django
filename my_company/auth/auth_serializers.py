from rest_framework import serializers
from my_company.models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from my_company.utils import *
import re
from my_company.phone_formats import *
from django.contrib.auth.hashers import make_password


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30,min_length=2, required=True, error_messages={'required': 'First name is required'})
    last_name = serializers.CharField(max_length=30,min_length=2, required=True, error_messages={'required': 'Last name is required'})
    phone = serializers.CharField(max_length=20,min_length=10, required=True, error_messages={'required': 'Phone is required'})
    country_code = serializers.ChoiceField(choices=COUNTRY_CODES_CHOICES, required=True, error_messages={'required': 'Country code is required'})
    company_headquarters = serializers.ChoiceField(choices=COUNTRIES_CHOICES, required=True, error_messages={'required': 'Company headquarters is required'})
    language = serializers.ChoiceField(choices=LANGUAGES_CHOICES, required=True, error_messages={'required': 'Language is required'})
    password = serializers.CharField(max_length=128,write_only=True,required=True,error_messages={'required': 'Password is required'})
    
    class Meta:
        model = MyInfo
        fields = ['email', 'password', 'first_name', 'last_name','country_code', 'phone', 'company_headquarters', 'language']
    
    def create(self, validated_data):
        # Hash the password before saving it
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        return super(RegistrationSerializer, self).create(validated_data)

    def validate_password(self, password):
        try:
            # Use Django's password validation to check if the password is valid
            validate_password(password, self.instance)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
                # Additional custom password validation
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase character.")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password must contain at least one lowercase character.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char in "!@#$%^&*()_+-={}[]|\\:;<>,.?/~" for char in password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return password
    
    # def validate_phone(self, phone):
    #     # Check if the phone contains only digits
    #     if not phone.isdigit():
    #         raise serializers.ValidationError("Phone number can only contain digits (0-9).")
    #     # Get the selected country code from the serializer
    #     country_code = self.initial_data.get('country_code')
    #     # Check if the country code is in the phone_formats dictionary
    #     if country_code in phone_formats:
    #         # Check if the phone number matches the expected format
    #         if not re.match(phone_formats[country_code], phone):
    #             raise serializers.ValidationError("Invalid phone number format for the selected country code.")
        
    #     return phone
    
    def validate_country_code(self, value):
        # Add custom validation logic for country_code here
        if value not in [code[0] for code in COUNTRY_CODES_CHOICES]:
            raise serializers.ValidationError("Invalid country code")
        return value

    def validate_company_headquarters(self, value):
        # Add custom validation logic for company_headquarters here
        if value not in [country[0] for country in COUNTRIES_CHOICES]:
            raise serializers.ValidationError("Invalid company headquarters")
        return value

    def validate_language(self, value):
        # Add custom validation logic for language here
        if value not in [language[0] for language in LANGUAGES_CHOICES]:
            raise serializers.ValidationError("Invalid language")
        return value
  
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={'required': 'Email is required'})
    password = serializers.CharField(required=True, error_messages={'required': 'Password is required'})


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={'required': 'Email is required'})


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,required=True, error_messages={'required': 'New password is required'})
    confirm_password = serializers.CharField(write_only=True,required=True, error_messages={'required': 'Confirm password is required'})







