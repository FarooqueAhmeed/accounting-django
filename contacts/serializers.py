from rest_framework import serializers
from contacts.models import *

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'  # You can specify the fields you want to include

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'  # You can specify the fields you want to include

class CombinedSerializer(serializers.Serializer):
    organizations = OrganizationSerializer(many=True)
    contacts = ContactSerializer(many=True)
