from contacts.models import *
from contacts.contacts.serializers import *
from my_company.my_info.serializers import *
from contacts.organization.serializers import *
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
from rest_framework.exceptions import ValidationError
from contacts.related_info.views import *




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def contact_api(request):
    if request.method == 'GET':
        return get_contacts(request)

    elif request.method == 'POST':
        return create_contact(request)

    elif request.method == 'PUT':
        return update_contact(request)

    elif request.method == 'DELETE':
        return delete_contact(request)

    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



def get_contacts(request):
    # Retrieve the authenticated user's MyInfo
    my_info = MyInfo.objects.get(email=request.user.email)

    if not my_info:
        return Response({'error': 'MyInfo not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)

    contact_id = request.data.get('id')

    if contact_id is not None:
        # Retrieve a specific contact by ID for the authenticated user
        contact = Contact.objects.filter(MyInfo=my_info, id=contact_id).first()

        if not contact:
            return Response({'error': 'Contact not found for the specified ID'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSerializer(contact)

        contact_type = contact.contact_type
        organization = contact.organization
        contact_type_name = contact_type.name if contact_type else None
        organization_name = organization.organization_name if organization else None

        response_data = {
            'message': 'Contact data fetched successfully.',
            'first_name': my_info.first_name,
            'contacts': [{
                **serializer.data,
                'contact_type_name': contact_type_name,
                'organization_name': organization_name,
            }],
            'MyInfo': MyInfoSerializer(my_info).data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    # Retrieve all contacts associated with the authenticated user
    contacts = Contact.objects.filter(MyInfo=my_info)
    serializer = ContactSerializer(contacts, many=True)

    response_data = {
        'message': 'Contacts data fetched successfully.',
        'first_name': my_info.first_name,
        'contacts': [],
        'MyInfo': MyInfoSerializer(my_info).data,
    }

    for contact in contacts:
        contact_type = contact.contact_type
        organization = contact.organization
        contact_type_name = contact_type.name if contact_type else None
        organization_name = organization.organization_name if organization else None

        # Find the corresponding serializer data based on contact id
        contact_data = next((c for c in serializer.data if c['id'] == contact.id), None)

        if contact_data:
            response_data['contacts'].append({
                **contact_data,
                'contact_type_name': contact_type_name,
                'organization_name': organization_name,
            })

    return Response(response_data, status=status.HTTP_200_OK)





def create_contact(request):
    # Assign the MyInfo based on the authenticated user
    my_info = MyInfo.objects.get(email=request.user.email)
    request.data['MyInfo'] = my_info.id

    # Validate the contact_type and organization
    contact_type_id = request.data.get('contact_type')
    organization_id = request.data.get('organization')

    # Check if contact_type is related to the authenticated user
    if contact_type_id:
        try:
            contact_type = Category.objects.get(id=contact_type_id, my_info=my_info)
        except Category.DoesNotExist:
            return Response({'error': 'Invalid contact type for the authenticated user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if organization is related to the authenticated user
    if organization_id:
        try:
            organization = Organization.objects.get(id=organization_id, MyInfo=my_info)
        except Organization.DoesNotExist:
            return Response({'error': 'Invalid organization for the authenticated user.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        # Validate and save the data
        serializer.save()

          # Retrieve the newly created contact
        contact = Contact.objects.get(id=serializer.data['id'])

        # Assuming 'Contact' is the newly created Contact
        contact_id = contact.id
        organization_id=None
        #start Address data creation
        # Check if address data is included in the request
        address_data = request.data.get('address_data')
        created_address = None
        try:
            created_address = create_address_data(address_data, organization_id,contact_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end Address data creation


        #start payment_information_for_contacts_data creation
        # Check if payment_information_for_contacts data is included in the request
        payment_information_for_contacts_data = request.data.get('payment_information_data')
        created_payment_information = None
        try:
            created_payment_information = create_payment_information_for_contacts_data(payment_information_for_contacts_data, organization_id,contact_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end payment_information_for_contacts data creation

        #start conditions data creation
        # Check if conditions data is included in the request
        conditions_data = request.data.get('conditions_data')
        created_conditions = None
        try:
            created_conditions = create_conditions_data(conditions_data, organization_id,contact_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end conditions data creation


             #start additional_information data creation
        # Check if additional_information data is included in the request
        additional_information_data = request.data.get('additional_information_data')
        created_additional_information = None
        try:
            created_additional_information = create_additional_information_data(additional_information_data, organization_id,contact_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end additional_information data creation

     
        # Include related data in the response
        contact_type_name = serializer.validated_data['contact_type'].name if serializer.validated_data.get('contact_type') else None
        organization_name = serializer.validated_data['organization'].organization_name if serializer.validated_data.get('organization') else None

        response_data = {
            'message': 'Contact created successfully.',
            'contact type name': contact_type_name,
            'organization name': organization_name,
            'data': serializer.data,
            'MyInfo': MyInfoSerializer(my_info).data,
        }

        #Start Address data creation
        if created_address:
            response_data['address_message'] = 'Address created successfully.'
            response_data['address'] = AddressForContactSerializer(created_address).data
        #end  Address data creation

         #start contact_details_data
        # Check if contact_details_data is included in the request
        contact_details_data = request.data.get('contact_details_data')
        # Check if contact_details_data is included in the request
        if contact_details_data:
            try:
                created_contact_details = create_contact_details_for_contact(contact_details_data, organization_id,contact_id)
                response_data['contact_message'] = 'Contact details created successfully.'
                response_data['contact_details'] = created_contact_details
            except ValidationError as e:
                return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        #end contact_details_data


        #Start payment_information_for_contacts_data creation
        if created_payment_information:
            response_data['payment_information_message'] = 'Payment information created successfully.'
            response_data['payment_information'] = PaymentInformationForContactsSerializer(created_payment_information).data
        #end payment_information_for_contacts_data creation

        #Start conditions data creation
        if created_conditions:
            response_data['conditions_message'] = 'Conditions created successfully.'
            response_data['conditions'] = ConditionsForContactsSerializer(created_conditions).data
        #end  conditions data creation

         #Start additional_information data creation
        if created_additional_information:
            response_data['additional_information_message'] = 'Additional information created successfully.'
            response_data['additional_information'] = AdditionalInformationSerializer(created_additional_information).data
        #end additional_information data creation

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def update_contact(request):
    # Retrieve the authenticated user's MyInfo
    my_info = MyInfo.objects.get(email=request.user.email)

    if not my_info:
        return Response({'error': 'MyInfo not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the contact to be updated
    contact_id = request.data.get('id')

    if contact_id is None:
        return Response({'error': 'Contact ID is required in the request data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        contact = Contact.objects.get(MyInfo=my_info, id=contact_id)
    except Contact.DoesNotExist:
        return Response({'error': 'Contact not found for the specified ID'}, status=status.HTTP_404_NOT_FOUND)

    # Check if request.user is updating their own contact data
    if contact.MyInfo != my_info:
        return Response({'error': 'You do not have permission to update this contact'}, status=status.HTTP_403_FORBIDDEN)

    # Ensure Contact.contact_type is related to request.user
    contact_type_id = request.data.get('contact_type')
    if contact_type_id is not None:
        try:
            contact_type = Category.objects.get(id=contact_type_id, my_info=my_info)
        except Category.DoesNotExist:
            return Response({'error': 'Invalid contact type for the authenticated user'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Ensure Contact.organization is related to request.user
    organization_id = request.data.get('organization')
    if organization_id is not None:
        try:
            organization = Organization.objects.get(id=organization_id, MyInfo=my_info)
        except Organization.DoesNotExist:
            return Response({'error': 'Invalid organization for the authenticated user'}, status=status.HTTP_400_BAD_REQUEST)

    # Serialize the request data using ContactSerializer
    serializer = ContactSerializer(contact, data=request.data, partial=True)

    if serializer.is_valid():
        # Validate and save the updated data
        serializer.save()


        #start address_data
        address_message = None  # Initialize address_message to None
        # Check if address data is included in the request
        address_data = request.data.get('address_data')

        if address_data:
            # Add the contact_id to the address data
            address_data['contact'] = contact_id

            # Find the address associated with the contact
            try:
                address = AddressForContact.objects.get(contact=contact)
                # Now, you have the address_id
                address_id = address.id
                        # Update the address using the found address_id
                try:
                    response = update_address_for_contact(request, address_id=address_id, data=address_data)
                except ValidationError as e:
                    return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
                address_message = 'Address updated successfully'
            except AddressForContact.DoesNotExist:
                    # Handle the case where no address is found for the organization
                    pass
            else:
                pass # No address data provided
                
            #end address_data

        
        #start contact_details_data
        contact_details_message = None  # Initialize address_message to None
        # Check if address data is included in the request
        contact_details_data = request.data.get('contact_details_data')

        if contact_details_data:
            # Add the organization ID to the contact_detail data
            contact_details_data['contact'] = contact_id
            # Find the ContactDetailsForContact associated with the organization
            try:
                contact_detail = ContactDetailsForContact.objects.get(contact=contact)
                # Now, you have the contact_detail_id
                contact_detail_id = contact_detail.id
                # Update the address using the found contact_detail_id
                try:
                    response = update_contact_details_for_contact(request, contact_detail_id=contact_detail_id, data=contact_details_data)
                except ValidationError as e:
                    return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
                contact_details_message = 'Contact detail updated successfully'
            except ContactDetailsForContact.DoesNotExist:
                    # Handle the case where no address is found for the organization
                    pass
            else:
                pass  # No address data provided
            #end contact_details_data

        #start payment_information_data
        payment_information_message = None  # Initialize payment_information_message to None
        # Check if payment_information data is included in the request
        payment_information_data = request.data.get('payment_information_data')
        if payment_information_data:
            # Add the contact ID to the payment_information data
            payment_information_data['contact'] = contact_id

            # Find the payment_information associated with the contact
            try:
                payment_information = PaymentInformationForContacts.objects.get(contact=contact)
                # Now, you have the payment_information_id
                payment_information_id = payment_information.id
                        # Update the payment_information using the found payment_information_id
                try:
                    response = update_payment_information_for_contacts(request, payment_information_id=payment_information_id, data=payment_information_data)
                except ValidationError as e:
                    return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
                payment_information_message = 'Payment information updated successfully'
            except PaymentInformationForContacts.DoesNotExist:
                # Handle the case where no Payment information is found for the organization
                pass
            else:
                pass  # No payment_information_message data provided
            #end payment_information_data

        #start conditions_data
        conditions_message = None  # Initialize conditions_message to None
        # Check if conditions data is included in the request
        conditions_data = request.data.get('conditions_data')

        if conditions_data:
            # Add the contact ID to the conditions data
            conditions_data['contact'] = contact_id

            # Find the conditions associated with the contact
            try:
                conditions = ConditionsForContacts.objects.get(contact=contact)

                # Now, you have the conditions_id
                conditions_id = conditions.id
                        # Update the conditions using the found conditions_id
                try:
                    response = update_conditions(request, conditions_id=conditions_id, data=conditions_data)
                except ValidationError as e:
                    return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
                conditions_message = 'Conditions updated successfully'
            except ConditionsForContacts.DoesNotExist:
                    # Handle the case where no conditions is found for the organization
                    pass
            else:
                pass  # No conditions data provided
            #end conditions_data

   #start additional_information_data
        additional_information_message = None  # Initialize additional_information_message to None
        # Check if additional_information data is included in the request
        additional_information_data = request.data.get('additional_information_data')

        if additional_information_data:
            # Add the contact ID to the additional_information data
            additional_information_data['contact'] = contact_id
                # Find the additional_information associated with the contact
            try:
                additional_information = AdditionalInformation.objects.get(contact=contact)
                # Now, you have the additional_information_id
                additional_information_id = additional_information.id
                # Update the additional_information using the found additional_information_id
                try:
                    response = update_additional_information(request, additional_information_id=additional_information_id, data=additional_information_data)
                except ValidationError as e:
                    return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
                additional_information_message = 'Additional information updated successfully'
            except AdditionalInformation.DoesNotExist:
                    # Handle the case where no additional_information is found for the organization
                    pass
            else:
                pass  # No additional_information data provided
            #end additional_information_data    



        response_data = {
           'message': 'Contact updated successfully.',
           'address_message':address_message,
            'contact_details_message':contact_details_message, 
            'payment_information_message': payment_information_message,
            'conditions_message': conditions_message,
            'additional_information_message': additional_information_message,
           'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def delete_contact(request):
    # Retrieve the authenticated user's MyInfo
    my_info = MyInfo.objects.get(email=request.user.email)

    if not my_info:
        return Response({'error': 'MyInfo not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the contact to be deleted
    contact_id = request.data.get('id')

    if contact_id is None:
        return Response({'error': 'Contact ID is required in the request data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        contact = Contact.objects.get(MyInfo=my_info, id=contact_id)
    except Contact.DoesNotExist:
        return Response({'error': 'Contact not found for the specified ID'}, status=status.HTTP_404_NOT_FOUND)

    # Check if request.user is deleting their own contact
    if contact.MyInfo != my_info:
        return Response({'error': 'You do not have permission to delete this contact'}, status=status.HTTP_403_FORBIDDEN)

    # Delete the contact
    contact.delete()

    return Response({'message': 'Contact deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)









