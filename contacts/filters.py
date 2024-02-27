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
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from itertools import chain
from contacts.serializers import *
from django.db.models import Q



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_contacts(request):
    if request.method != 'GET':
        return Response({'error': 'Invalid request method. Use GET.'}, status=status.HTTP_400_BAD_REQUEST)

    # Filter organizations and contacts based on request.user, and order them by '-created'
    organizations = Organization.objects.filter(MyInfo=request.user).order_by('-created')
    contacts = Contact.objects.filter(MyInfo=request.user).order_by('-created')

    data = {}

    if not organizations and not contacts:
        data['message'] = 'No organizations and contacts available for the user.'
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    # Combine organizations and contacts into a single list and sort by '-created'
    all_objects = sorted(
        chain((obj for obj in organizations), (obj for obj in contacts)),
        key=lambda obj: obj.created,
        reverse=True
    )

    # Create a paginator and paginate the sorted list of objects
    paginator = PageNumberPagination()
    paginator.page_size = 50  # You can adjust the page size as needed

    result_page = paginator.paginate_queryset(all_objects, request)
    object_serializer = []

    for obj in result_page:
        serialized_data = {}
        if isinstance(obj, Organization):
            org_data = OrganizationSerializer(obj).data
            org_data['created'] = obj.created.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            serialized_data.update(org_data)
            serialized_data['object_type'] = 'organization'
        elif isinstance(obj, Contact):
            contact_data = ContactSerializer(obj).data
            contact_data['created'] = obj.created.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            serialized_data.update(contact_data)
            serialized_data['object_type'] = 'contact'

        # Retrieve and append country value from AddressForContact
        addresses = AddressForContact.objects.filter(organization=obj) if isinstance(obj, Organization) else AddressForContact.objects.filter(contact=obj)
        if addresses:
            country = addresses[0].country
            serialized_data['country'] = country

        # Retrieve and append tags from AdditionalInformation
        additional_info = AdditionalInformation.objects.filter(organization=obj) if isinstance(obj, Organization) else AdditionalInformation.objects.filter(contact=obj)
        if additional_info:
            tags = additional_info[0].tags
            serialized_data['tags'] = tags

        object_serializer.append(serialized_data)

    data['objects'] = object_serializer

    # Retrieve unique Category.name values related to Organization.contact_type and Contact.contact_type
    category_names = Category.objects.filter(name__in=[org.contact_type.name for org in organizations] +
                                                    [contact.contact_type.name for contact in contacts]).distinct().values_list('name', flat=True)
    data['category_names'] = list(category_names)

    # Include pagination information in the response
    data['pagination'] = {
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'count': paginator.page.paginator.count,
        'displayed_count': len(object_serializer),  # Number of entries being displayed
    }
    data['success'] = 'Data retrieved successfully.'
    return Response(data, status=status.HTTP_200_OK)






@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contacts_by_type(request):
    if request.method != 'GET':
        return Response({'error': 'Invalid request method. Use GET.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the contact_type from the request JSON
    contact_type = request.data.get('contact_type', None)

    if not contact_type:
        return Response({'error': 'contact type parameter is required in the request JSON.'}, status=status.HTTP_400_BAD_REQUEST)

    # Filter organizations and contacts based on request.user and contact_type, and order them by '-created'
    organizations = Organization.objects.filter(MyInfo=request.user, contact_type__name=contact_type).order_by('-created')
    contacts = Contact.objects.filter(MyInfo=request.user, contact_type__name=contact_type).order_by('-created')

    data = {}

    if not organizations and not contacts:
        data['message'] = f'No organizations and contacts available for the user with contact_type: {contact_type}.'
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    # Combine organizations and contacts into a single list and sort by '-created'
    all_objects = sorted(
        chain((obj for obj in organizations), (obj for obj in contacts)),
        key=lambda obj: obj.created,
        reverse=True
    )

    # Create a paginator and paginate the sorted list of objects
    paginator = PageNumberPagination()
    paginator.page_size = 50  # You can adjust the page size as needed

    result_page = paginator.paginate_queryset(all_objects, request)
    object_serializer = []

    for obj in result_page:
        serialized_data = {}
        if isinstance(obj, Organization):
            org_data = OrganizationSerializer(obj).data
            org_data['created'] = obj.created.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            serialized_data.update(org_data)
            serialized_data['object_type'] = 'organization'
        elif isinstance(obj, Contact):
            contact_data = ContactSerializer(obj).data
            contact_data['created'] = obj.created.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            serialized_data.update(contact_data)
            serialized_data['object_type'] = 'contact'

        # Retrieve and append country value from AddressForContact
        addresses = AddressForContact.objects.filter(organization=obj) if isinstance(obj, Organization) else AddressForContact.objects.filter(contact=obj)
        if addresses:
            country = addresses[0].country
            serialized_data['country'] = country

        # Retrieve and append tags from AdditionalInformation
        additional_info = AdditionalInformation.objects.filter(organization=obj) if isinstance(obj, Organization) else AdditionalInformation.objects.filter(contact=obj)
        if additional_info:
            tags = additional_info[0].tags
            serialized_data['tags'] = tags

        object_serializer.append(serialized_data)

    data['objects'] = object_serializer

    # Retrieve unique Category.name values related to the specified contact_type
    category_names = Category.objects.filter(name=contact_type).distinct().values_list('name', flat=True)
    data['category_names'] = list(category_names)

    # Include pagination information in the response
    data['pagination'] = {
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'count': paginator.page.paginator.count,
        'displayed_count': len(object_serializer),  # Number of entries being displayed
    }
    data['success'] = f'Data retrieved successfully for contact type: {contact_type}.'
    return Response(data, status=status.HTTP_200_OK)





@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filter_contacts(request):
    if request.method != 'GET':
        return Response({'error': 'Invalid request method. Use GET.'}, status=status.HTTP_400_BAD_REQUEST)

    # Initialize lists to store filtered organizations and contacts
    filtered_organizations = []
    filtered_contacts = []

    # Get values from the request query parameters
    name = request.data.get('name', None)
    country = request.data.get('country', None)
    ZIP_code = request.data.get('ZIP_code', None)
    city = request.data.get('city', None)
    tags = request.data.get('tags', None)

    show_all = request.data.get('show_all', None)
    show_only_contacts = request.data.get('show_only_contacts', None)
    show_only_organizations = request.data.get('show_only_organizations', None)

    if name:
        # Apply filters based on the 'name' value if it's present in the query parameters
        name_organizations = Organization.objects.filter(MyInfo=request.user, organization_name__icontains=name)
        name_contacts = Contact.objects.filter(MyInfo=request.user, first_name__icontains=name)
        if show_all:
            filtered_organizations.extend(name_organizations)
            filtered_contacts.extend(name_contacts)
        elif show_only_contacts:
            filtered_contacts.extend(name_contacts)
        elif show_only_organizations:
            filtered_organizations.extend(name_organizations)

    elif country:
        # Apply filters based on the 'country' value if it's present in the query parameters
        org_addresses = AddressForContact.objects.filter(country__contains=country, organization__MyInfo=request.user)
        contact_addresses = AddressForContact.objects.filter(country__contains=country, contact__MyInfo=request.user)
        country_organizations = Organization.objects.filter(addressforcontact__in=org_addresses)
        country_contacts = Contact.objects.filter(addressforcontact__in=contact_addresses)
        if show_all:
            filtered_organizations.extend(country_organizations)
            filtered_contacts.extend(country_contacts)
        elif show_only_contacts:
            filtered_contacts.extend(country_contacts)
        elif show_only_organizations:
            filtered_organizations.extend(country_organizations)

    elif ZIP_code:
        # Apply filters based on the 'ZIP_code' value if it's present in the query parameters
        org_addresses = AddressForContact.objects.filter(ZIP_code__contains=ZIP_code, organization__MyInfo=request.user)
        contact_addresses = AddressForContact.objects.filter(ZIP_code__contains=ZIP_code, contact__MyInfo=request.user)
        ZIP_code_organizations = Organization.objects.filter(addressforcontact__in=org_addresses)
        ZIP_code_contacts = Contact.objects.filter(addressforcontact__in=contact_addresses)
        if show_all:
            filtered_organizations.extend(ZIP_code_organizations)
            filtered_contacts.extend(ZIP_code_contacts)
        elif show_only_contacts:
            filtered_contacts.extend(ZIP_code_contacts)
        elif show_only_organizations:
            filtered_organizations.extend(ZIP_code_organizations)

    elif city:
        # Apply filters based on the 'city' value if it's present in the query parameters
        org_addresses = AddressForContact.objects.filter(city__contains=city, organization__MyInfo=request.user)
        contact_addresses = AddressForContact.objects.filter(city__contains=city, contact__MyInfo=request.user)
        city_organizations = Organization.objects.filter(addressforcontact__in=org_addresses)
        city_contacts = Contact.objects.filter(addressforcontact__in=contact_addresses)
        if show_all:
            filtered_organizations.extend(city_organizations)
            filtered_contacts.extend(city_contacts)
        elif show_only_contacts:
            filtered_contacts.extend(city_contacts)
        elif show_only_organizations:
            filtered_organizations.extend(city_organizations)
    elif tags:
        # Apply filters based on the 'tags' value if it's present in the query parameters 
        org_addresses = AdditionalInformation.objects.filter(tags__contains=tags, organization__MyInfo=request.user)
        contact_addresses = AdditionalInformation.objects.filter(tags__contains=tags, contact__MyInfo=request.user)
        tags_organizations = Organization.objects.filter(additionalinformation__in=org_addresses)
        tags_contacts = Contact.objects.filter(additionalinformation__in=contact_addresses)
        if show_all:
            filtered_organizations.extend(tags_organizations)
            filtered_contacts.extend(tags_contacts)
        elif show_only_contacts:
            filtered_contacts.extend(tags_contacts)
        elif show_only_organizations:
            filtered_organizations.extend(tags_organizations)        
    else:
        # Filter organizations and contacts based on request.user, and order them by '-created'
        filtered_organizations = Organization.objects.filter(MyInfo=request.user).order_by('-created')
        filtered_contacts = Contact.objects.filter(MyInfo=request.user).order_by('-created')


    
    # Combine filtered organizations and contacts into a single list
    all_objects = sorted(
        chain(filtered_organizations, filtered_contacts),
        key=lambda obj: obj.created,
        reverse=True
    )

    # Create a paginator and paginate the sorted list of objects
    paginator = PageNumberPagination()
    paginator.page_size = 50  # You can adjust the page size as needed

    result_page = paginator.paginate_queryset(all_objects, request)
    object_serializer = []

    for obj in result_page:
        serialized_data = {}
        if isinstance(obj, Organization):
            org_data = OrganizationSerializer(obj).data
            org_data['created'] = obj.created.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            serialized_data.update(org_data)
            serialized_data['object_type'] = 'organization'
        elif isinstance(obj, Contact):
            contact_data = ContactSerializer(obj).data
            contact_data['created'] = obj.created.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
            serialized_data.update(contact_data)
            serialized_data['object_type'] = 'contact'

        # Retrieve and append country value from AddressForContact
        addresses = AddressForContact.objects.filter(organization=obj) if isinstance(obj, Organization) else AddressForContact.objects.filter(contact=obj)
        if addresses:
            country = addresses[0].country
            serialized_data['country'] = country

        # Retrieve and append tags from AdditionalInformation
        additional_info = AdditionalInformation.objects.filter(organization=obj) if isinstance(obj, Organization) else AdditionalInformation.objects.filter(contact=obj)
        if additional_info:
            tags = additional_info[0].tags
            serialized_data['tags'] = tags

        object_serializer.append(serialized_data)

    data = {}
    data['objects'] = object_serializer

    # Retrieve unique Category.name values related to Organization.contact_type and Contact.contact_type
    data['category_names'] = []

    if filtered_organizations:
        category_names_org = Category.objects.filter(
            name__in=[org.contact_type.name for org in filtered_organizations]
        ).distinct().values_list('name', flat=True)
        data['category_names'].extend(category_names_org)

    if filtered_contacts:
        category_names_contact = Category.objects.filter(
            name__in=[contact.contact_type.name for contact in filtered_contacts]
        ).distinct().values_list('name', flat=True)
        data['category_names'].extend(category_names_contact)

    # Remove duplicates from category_names
    data['category_names'] = list(set(data['category_names']))

    # Include pagination information in the response
    data['pagination'] = {
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'count': paginator.page.paginator.count,
        'displayed_count': len(object_serializer),  # Number of entries being displayed
    }
    data['message'] = 'Data retrieved successfully.'
    return Response(data, status=status.HTTP_200_OK)




