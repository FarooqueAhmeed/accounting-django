from rest_framework import serializers
from contacts.models import *
from django.core.exceptions import ValidationError


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ('name',)  # Assuming 'name' is the field you want to include


class NotesSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.organization_name', read_only=True, default=None)
    contact_first_name = serializers.CharField(source='contact.first_name', read_only=True, default=None)
    staff_for_email_notification = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Staff.objects.all(),
    ) 

    staff_for_email_notification_names = serializers.SerializerMethodField()

    def get_staff_for_email_notification_names(self, obj):
        staff_names = []
        for staff in obj.staff_for_email_notification.all():
            staff_names.append(staff.name)
        return staff_names
    
    class Meta:
        model = Notes
        fields = '__all__'
        extra_kwargs = {'staff_for_email_notification': {'write_only': False}}

    def update(self, instance, validated_data):
        # Handle the staff_for_email_notification many-to-many field
        staff_for_email_notification = validated_data.pop('staff_for_email_notification', None)
        if staff_for_email_notification is not None:
            instance.staff_for_email_notification.set(staff_for_email_notification)
        
        # Update the rest of the fields
        return super().update(instance, validated_data)
    
    def validate_attachment(self, value):
        """
        Check that the file is a PDF, JPEG, or PNG.
        """
        if value:  # if a file is provided
            # Define the list of valid mime types
            valid_mime_types = [
                'application/pdf', 
                'application/x-pdf', 
                'image/jpeg', 
                'image/pjpeg', 
                'image/png'
            ]
            # Get the uploaded file's mime type
            file_mime_type = value.content_type
            if file_mime_type not in valid_mime_types:
                raise serializers.ValidationError(
                    'Unsupported file type. Supported types are: PDF, JPEG, and PNG.'
                )
        return value