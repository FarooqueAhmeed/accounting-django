from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.http import Http404
from django.http import HttpRequest
from rest_framework.request import Request
from django.core.exceptions import PermissionDenied
from my_company.my_info.serializers import *
from contacts.models import *
from contacts.organization.serializers import *
from my_company.models import *
from contacts.related_info.serializers import *
from rest_framework.exceptions import ValidationError




def create_address_data(address_data, organization_id=None, contact_id=None):
    if address_data:
        if organization_id:
            # If organization_id is provided, use it as the related organization
            address_data['organization'] = organization_id
        elif contact_id:
            # If contact_id is provided, use it as the related contact
            address_data['contact'] = contact_id 
        else:
           pass

        # Create and save the address using AddressForContactSerializer
        address_serializer = AddressForContactSerializer(data=address_data)
        if address_serializer.is_valid():
            created_address = address_serializer.save()
            return created_address
        else:
            raise ValidationError(address_serializer.errors)
    else:
        pass

def update_address_for_contact(request, address_id, data):
    try:
        address = AddressForContact.objects.get(pk=address_id)
    
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            raise ValidationError('Authentication required.')
        try:
            # Check if the address is related to the user
            if address.organization.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this address.')
        except:
             # Check if the address is related to the user
            if address.contact.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this address.')

        # Update the address with the provided data
        serializer = AddressForContactSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return address  # Return the updated address
        else:
            raise ValidationError(serializer.errors)
    except AddressForContact.DoesNotExist:
        pass






def create_contact_details_for_contact(contact_details_data,organization_id=None, contact_id=None):

    if organization_id:
        # Assign the organization to the contact details data
        contact_details_data['organization'] = organization_id
    elif contact_id:
            # If contact_id is provided, use it as the related contact
            contact_details_data['contact'] = contact_id 
    else:
        pass
    
    serializer = ContactDetailsForContactSerializer(data=contact_details_data)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValidationError(serializer.errors)



def update_contact_details_for_contact(request, contact_detail_id,data):
    try:
        contact_details = ContactDetailsForContact.objects.get(pk=contact_detail_id)
    
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            # Check if the contact_details is related to the user
            if contact_details.organization.MyInfo != request.user:
                return Response({'error': 'You do not have permission to update this contact details.'}, status=status.HTTP_403_FORBIDDEN)
        except:
            if contact_details.contact.MyInfo != request.user:
                return Response({'error': 'You do not have permission to update this contact details.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the contact details with the provided data
        serializer = ContactDetailsForContactSerializer(contact_details, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_contact_details = serializer.instance  # Get the updated contact_details
            return updated_contact_details
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ContactDetailsForContact.DoesNotExist:
        pass





def create_payment_information_for_contacts_data(payment_information_for_contacts_data, organization_id=None, contact_id=None):
    if payment_information_for_contacts_data:
        if organization_id:
            payment_information_for_contacts_data['organization'] = organization_id  # Assuming 'organization' is the related field 
        elif contact_id:
                # If contact_id is provided, use it as the related contact
                payment_information_for_contacts_data['contact'] = contact_id 
        else:
            pass
        # Create and save the payment_information_for_contacts_data using PaymentInformationForContactsSerializer
        payment_information_serializer = PaymentInformationForContactsSerializer(data=payment_information_for_contacts_data)
        if payment_information_serializer.is_valid():
            created_payment_information = payment_information_serializer.save()
            return created_payment_information
        else:
            raise ValidationError(payment_information_serializer.errors)
        

def update_payment_information_for_contacts(request, payment_information_id, data):
    try:
        payment_information = PaymentInformationForContacts.objects.get(pk=payment_information_id)
    
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            raise ValidationError('Authentication required.')
        try:
            # Check if the payment_information is related to the user
            if payment_information.organization.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this payment information.')
        except:
            if payment_information.contact.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this payment information.')

        # Update the payment_information with the provided data
        serializer = PaymentInformationForContactsSerializer(payment_information, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return payment_information  # Return the updated payment_information
        else:
            raise ValidationError(serializer.errors)
    except PaymentInformationForContacts.DoesNotExist:
        pass



def create_conditions_data(conditions_data, organization_id=None, contact_id=None):
    if conditions_data:
        if organization_id:
            conditions_data['organization'] = organization_id  # Assuming 'organization' is the related field in ConditionsForContact
        elif contact_id:
                # If contact_id is provided, use it as the related contact
                conditions_data['contact'] = contact_id 
        else:
            pass
        # Create and save the conditions using ConditionsForContactsSerializer
        conditions_serializer = ConditionsForContactsSerializer(data=conditions_data)
        if conditions_serializer.is_valid():
            created_conditions = conditions_serializer.save()
            return created_conditions
        else:
            raise ValidationError(conditions_serializer.errors)



def update_conditions(request, conditions_id, data):
    try:
        conditions = ConditionsForContacts.objects.get(pk=conditions_id)
    
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            raise ValidationError('Authentication required.')
        try:
            # Check if the conditions is related to the user
            if conditions.organization.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this conditions.')
        except:
            if conditions.contact.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this conditions.')

        # Update the conditions with the provided data
        serializer = ConditionsForContactsSerializer(conditions, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return conditions  # Return the updated conditions
        else:
            raise ValidationError(serializer.errors)
    except ConditionsForContacts.DoesNotExist:
        pass



def create_additional_information_data(additional_information_data, organization_id=None, contact_id=None):
    if additional_information_data:

        if organization_id:
            additional_information_data['organization'] = organization_id  # Assuming 'organization' is the related field in AdditionalInformation
        elif contact_id:
            # If contact_id is provided, use it as the related contact
            additional_information_data['contact'] = contact_id 
        else:
            pass
        # Create and save the additional_information using AdditionalInformationSerializer
        additional_information_serializer = AdditionalInformationSerializer(data=additional_information_data)
        if additional_information_serializer.is_valid():
            created_additional_information = additional_information_serializer.save()
            return created_additional_information
        else:
            raise ValidationError(additional_information_serializer.errors)





def update_additional_information(request, additional_information_id, data):
    try:
        additional_information = AdditionalInformation.objects.get(pk=additional_information_id)
    
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            raise ValidationError('Authentication required.')
        try:
            # Check if the additional_information is related to the user
            if additional_information.organization.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this additional information.')
        except:
            # Check if the additional_information is related to the user
            if additional_information.contact.MyInfo != request.user:
                raise PermissionDenied('You do not have permission to update this additional information.')    

        # Update the additional_information with the provided data
        serializer = AdditionalInformationSerializer(additional_information, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return additional_information  # Return the updated additional_information
        else:
            raise ValidationError(serializer.errors)
    except AdditionalInformation.DoesNotExist:
        pass
















