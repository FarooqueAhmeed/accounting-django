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
from contacts.related_info.views import *
from rest_framework.exceptions import ValidationError



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def organization_api(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return get_organizations(request)
        
    elif request.method == 'POST':
            return create_organization(request)
    elif request.method == 'PUT':
        return update_organization(request)

    elif request.method == 'DELETE':
        return delete_organization_by_id(request)
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_organizations(request):
    # Retrieve the authenticated user's info
    user_info = MyInfo.objects.get(email=request.user.email)

    if user_info:
        organization_id = request.data.get('id')
   
        if organization_id is not None:
            # Retrieve a specific Organization by ID for the authenticated user
            organization = Organization.objects.filter(MyInfo=user_info, id=organization_id).first()

            if organization:
                serializer = OrganizationSerializer(organization)
                # Retrieve related contacts
                related_contacts = Contact.objects.filter(organization=organization)
                contacts_serializer = ContactSerializer(related_contacts, many=True)

                # Include related data in the response
                response_data = {
                    'message': 'Organization data fetched successfully.',
                    'user_info': MyInfoSerializer(user_info).data,
                    'organization': serializer.data,
                    'contact_type': organization.contact_type.name,  # Assuming you want the ID of the contact_type
                    'contacts': [contact.first_name for contact in related_contacts],  # List of contact IDs
                    'contacts_details': contacts_serializer.data,  # Serialized contact details
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Organization not found for the specified ID'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all Organizations associated with the authenticated user
        organizations = Organization.objects.filter(MyInfo=user_info)
        serializer = OrganizationSerializer(organizations, many=True)

        # Include related data in the response for all organizations
        organizations_data = []
        for organization in organizations:
            contacts = Contact.objects.filter(organization=organization)
            contacts_serializer = ContactSerializer(contacts, many=True)
            organization_data = {
                'id': organization.id,
                'organization_name': organization.organization_name,
                'name_suffix': organization.name_suffix,
                'customer_number': organization.customer_number,
                'debtor_number': organization.debtor_number,
                'contact_type': organization.contact_type.name,
                'contacts': [contact.first_name for contact in contacts],
                'contacts_details': contacts_serializer.data,
            }
            organizations_data.append(organization_data)

        response_data = {
            'message': 'Organizations data fetched successfully.',
            'user_info': MyInfoSerializer(user_info).data,
            'organizations': organizations_data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    return Response({'error': 'User info not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)



def create_organization(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Create a new Organization for the authenticated user
    request_data = request.data.copy()
    request_data['MyInfo'] = request.user.id

    # Validate the contact_type
    contact_type_id = request_data.get('contact_type')
    if contact_type_id is not None:
        try:
            contact_type = Category.objects.get(id=contact_type_id, my_info=request.user)
        except Category.DoesNotExist:
            return Response({'error': 'Invalid contact_type for the authenticated user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the contacts
    contact_ids = request_data.get('contacts', [])
    invalid_contact_ids = [contact_id for contact_id in contact_ids if not Contact.objects.filter(id=contact_id, MyInfo=request.user).exists()]
    if invalid_contact_ids:
        return Response({'error': 'Invalid contacts for the authenticated user: {}'.format(invalid_contact_ids)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrganizationSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()

        # Retrieve the newly created organization
        organization = Organization.objects.get(id=serializer.data['id'])

        # Assuming 'organization' is the newly created organization
        organization_id = organization.id


        #start Address data creation

        # Check if address data is included in the request
        address_data = request.data.get('address_data')
        created_address = None
        try:
            created_address = create_address_data(address_data,organization_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end Address data creation

        #start payment_information_for_contacts_data creation

        # Check if payment_information_for_contacts data is included in the request
        payment_information_for_contacts_data = request.data.get('payment_information_data')
        created_payment_information = None
        try:
            created_payment_information = create_payment_information_for_contacts_data(payment_information_for_contacts_data, organization_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end payment_information_for_contacts data creation

               #start conditions data creation
        # Check if conditions data is included in the request
        conditions_data = request.data.get('conditions_data')
        created_conditions = None
        try:
            created_conditions = create_conditions_data(conditions_data, organization_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end conditions data creation

         #start additional_information data creation
        # Check if additional_information data is included in the request
        additional_information_data = request.data.get('additional_information_data')
        created_additional_information = None
        try:
            created_additional_information = create_additional_information_data(additional_information_data, organization_id)
        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        #end additional_information data creation





        # Retrieve related contacts
        related_contacts = Contact.objects.filter(organization=organization)

        # Serialize the organization and related contacts
        organization_serializer = OrganizationSerializer(organization)
        contacts_serializer = ContactSerializer(related_contacts, many=True)

        response_data = {
            'message': 'Organization created successfully.',
            'organization': organization_serializer.data,
            'contacts': contacts_serializer.data,
            'contact_type': contact_type_id,
            'user_info': MyInfoSerializer(request.user).data,
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
                created_contact_details = create_contact_details_for_contact(contact_details_data, organization_id)
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



def update_organization(request):
    try:
        organization_id = request.data.get('id')
        user = request.user
        print(organization_id)
        print(user)


        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        organization = Organization.objects.get(pk=organization_id, MyInfo=user)
        if organization.MyInfo != user:
            return Response({'error': 'You do not have permission to update this organization.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the request data with the authenticated user's ID
        request_data = request.data.copy()
        request_data['MyInfo'] = user.id

        # Validate the contact_type
        contact_type_id = request_data.get('contact_type')
        if contact_type_id:
            contact_type = Category.objects.filter(id=contact_type_id, my_info=user).first()
            if not contact_type:
                return Response({'error': 'Invalid contact type for the authenticated user'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the contacts
        contact_ids = request_data.get('contacts', [])
        invalid_contact_ids = [contact_id for contact_id in contact_ids if not Contact.objects.filter(id=contact_id, MyInfo=user).exists()]
        if invalid_contact_ids:
            return Response({'error': f'Invalid contact IDs for the authenticated user: {", ".join(map(str, invalid_contact_ids))}'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure all contacts are related to the same user
        contact_my_infos = Contact.objects.filter(id__in=contact_ids).values_list('MyInfo', flat=True)
        if len(set(contact_my_infos)) != 1:
            raise PermissionDenied('Contacts must belong to the same user.')

        serializer = OrganizationSerializer(organization, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Get the organization's ID
            organization_id = organization.id
             
             #start address_data
            address_message = None  # Initialize address_message to None
            # Check if address data is included in the request
            address_data = request.data.get('address_data')

            if address_data:
                # Add the organization ID to the address data
                address_data['organization'] = organization_id

                # Find the address associated with the organization
                try:
                    address = AddressForContact.objects.get(organization=organization)

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
                address_message = None  # No address data provided
            #end address_data


            #start contact_details_data
            contact_details_message = None  # Initialize address_message to None
            # Check if address data is included in the request
            contact_details_data = request.data.get('contact_details_data')

            if contact_details_data:
                # Add the organization ID to the contact_detail data
                contact_details_data['organization'] = organization_id

                # Find the ContactDetailsForContact associated with the organization
                try:
                    contact_detail = ContactDetailsForContact.objects.get(organization=organization)

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
                contact_details_message = None  # No address data provided
            #end contact_details_data

             #start payment_information_data
            payment_information_message = None  # Initialize payment_information_message to None
            # Check if payment_information data is included in the request
            payment_information_data = request.data.get('payment_information_data')

            if payment_information_data:
                # Add the organization ID to the payment_information data
                payment_information_data['organization'] = organization_id

                # Find the payment_information associated with the organization
                try:
                    payment_information = PaymentInformationForContacts.objects.get(organization=organization)

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
                payment_information_message = None  # No payment_information_message data provided
            #end payment_information_data

               #start conditions_data
            conditions_message = None  # Initialize conditions_message to None
            # Check if conditions data is included in the request
            conditions_data = request.data.get('conditions_data')

            if conditions_data:
                # Add the organization ID to the conditions data
                conditions_data['organization'] = organization_id

                # Find the conditions associated with the organization
                try:
                    conditions = ConditionsForContacts.objects.get(organization=organization)

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
                conditions_message = None  # No conditions data provided
            #end conditions_data


             #start additional_information_data
            additional_information_message = None  # Initialize additional_information_message to None
            # Check if additional_information data is included in the request
            additional_information_data = request.data.get('additional_information_data')

            if additional_information_data:
                # Add the organization ID to the additional_information data
                additional_information_data['organization'] = organization_id

                # Find the additional_information associated with the organization
                try:
                    additional_information = AdditionalInformation.objects.get(organization=organization)

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
                additional_information_message = None  # No additional_information data provided
            #end additional_information_data    





            # Retrieve related contacts
            related_contacts = Contact.objects.filter(organization=organization)

            # Serialize the organization and related contacts
            organization_serializer = OrganizationSerializer(organization)
            contacts_serializer = ContactSerializer(related_contacts, many=True)

            response_data = {
                'message': 'Organization updated successfully.',
                'address_message': address_message,
                'contact_details_message':contact_details_message,
                'payment_information_message': payment_information_message,
                'conditions_message': conditions_message,
                'additional_information_message': additional_information_message,
                'organization': organization_serializer.data,
                'contacts': contacts_serializer.data,
                'contact_type': contact_type_id,
                'user_info': MyInfoSerializer(user).data,

            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Organization.DoesNotExist:
        return Response({'error': 'Organization not found for the specified ID'}, status=status.HTTP_404_NOT_FOUND)




def delete_organization_by_id(request):
    organization_id = request.data.get('id')
    try:
        # Retrieve a specific Organization by ID
        organization = Organization.objects.get(pk=organization_id)
    except Organization.DoesNotExist:
        return Response({'error': 'Organization not found for the specified ID'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the organization is related to the authenticated user
    if organization.MyInfo != request.user:
        return Response({'error': 'Permission denied. You can only delete your own organizations.'}, status=status.HTTP_403_FORBIDDEN)

    organization.delete()
    return Response({'message': 'Organization deleted successfully'}, status=status.HTTP_204_NO_CONTENT)













