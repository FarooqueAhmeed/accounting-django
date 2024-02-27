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
from contacts.notes.serializers import *
import django.core.mail
from .serializers import LettersSerializer
from rest_framework.parsers import JSONParser




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_letters(request):
    if request.method == 'GET':
        return get_letters(request)
    elif request.method == 'POST':
        return post_letter(request)
    elif request.method == 'PUT':
        return put_letter(request)
    elif request.method == 'DELETE':
        return delete_letter(request)

def get_letters(request):
    #incoming data to get the 'id'
    letter_id = request.data.get('id')

    # If an 'id' is provided, try to retrieve a specific letter
    if letter_id:
        try:
            letter = Letters.objects.get(pk=letter_id, MyInfo=request.user)
        except Letters.DoesNotExist:
            return Response({'message': 'Letter not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the single letter instance
        serializer = LettersSerializer(letter, context={'request': request})
        return Response({
            'message': 'Letter retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        # If no 'id' is provided, retrieve all letters for the user
        letters = Letters.objects.filter(MyInfo=request.user)

        if not letters:
            return Response({'message': 'No letters found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the letter queryset
        serializer = LettersSerializer(letters, many=True, context={'request': request})
        return Response({
            'message': 'Letters retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


def post_letter(request):
    # Create a mutable copy of the request data to modify
    data = request.data.copy()
    organization_id = data.get('organization')
    contact_id = data.get('contact')

    # At least one of organization or contact must be provided
    if organization_id is None and contact_id is None:
        return Response(
            {'message': 'An organization or contact must be provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Automatically assign MyInfo to request.user
    data['MyInfo'] = request.user.pk

    # Initialize the serializer with the modified data
    serializer = LettersSerializer(data=data)

    # Validate and save the serializer
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def put_letter(request):
    data = request.data.copy()

        # Check if 'organization_id' or 'contact_id' is provided and update accordingly
    organization_id = data.get('organization')
    contact_id = data.get('contact')

        # At least one of organization or contact must be provided
    if organization_id is None and contact_id is None:
        return Response(
            {'message': 'An organization or contact must be provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update organization or contact based on provided IDs, if not provided, set to None
    if organization_id is not None:
        data['organization'] = organization_id
    else:
        data['organization'] = None

    if contact_id is not None:
        data['contact'] = contact_id
    else:
        data['contact'] = None

    try:
        letter = Letters.objects.get(pk=data.get('id'),MyInfo=request.user)
    except Letters.DoesNotExist:
        return Response({'message': 'The letter does not exist'}, status=404)
    
    # Automatically assign MyInfo to request.user
    data['MyInfo'] = request.user.pk
    serializer = LettersSerializer(letter, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

def delete_letter(request):
    data = request.data.copy()
    try:
        letter = Letters.objects.get(pk=data['id'],MyInfo=request.user)
        letter.delete()
        return Response({'message': 'Letter was deleted successfully!'}, status=204)
    except Letters.DoesNotExist:
        return Response({'message': 'The letter does not exist'}, status=404)

