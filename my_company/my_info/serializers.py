from rest_framework import serializers
from my_company.models import MyInfo
from my_company.choices_LANGUAGES_COUNTRIES import *

class MyInfoUpdateSerializer(serializers.ModelSerializer):
    salutation = serializers.ChoiceField(choices=MyInfo.SALUTATION_CHOICES,required=True,error_messages={'required': 'Salutation is required'})
    first_name = serializers.CharField(max_length=255,min_length=2,required=True,error_messages={'required': 'First name is required'})
    last_name = serializers.CharField(max_length=255,min_length=2, required=True,error_messages={'required': 'Last name is required'})
    email = serializers.EmailField(required=True,error_messages={'required': 'Email is required'})
    language = serializers.ChoiceField(choices=LANGUAGES_CHOICES,required=True,error_messages={'required': 'Language is required'})
    abbreviation = serializers.CharField(max_length=10,required=True,error_messages={'required': 'Abbreviation is required'})

    class Meta:
        model = MyInfo
        fields = ['salutation', 'first_name', 'last_name', 'email', 'language', 'abbreviation']




class MyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyInfo
        fields = '__all__'