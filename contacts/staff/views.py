from contacts.models import *
from contacts.staff.serializers import *
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




@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_staff(request):
    if request.method == 'GET':
        return get_staff(request)
    elif request.method == 'POST':
        return create_staff(request)
    elif request.method == 'PUT':
        return update_staff(request)
    elif request.method == 'DELETE':
        return delete_staff(request)
    else:
        return Response({'detail': 'Invalid request method'}, status=405)


def get_staff(request):
    staff_id = request.data.get('id')
    
    if staff_id:
        try:
            staff = Staff.objects.get(id=staff_id, MyInfo=request.user)
        except Staff.DoesNotExist:
            raise Http404

        serializer = StaffSerializer(staff)
        user_data = {
            'user_data': {
                'email': request.user.email,
                'first_name': request.user.first_name,
            }
        }
        return Response({'message': 'Staff data retrieved successfully', **user_data, 'staff': serializer.data})
    else:
        staff = Staff.objects.filter(MyInfo=request.user)
        serializer = StaffSerializer(staff, many=True)
        user_data = {
            'user_data': {
                'email': request.user.email,
                'first_name': request.user.first_name,
            }
        }
        return Response({'message': 'Staff data retrieved successfully', **user_data, 'staff': serializer.data})


def create_staff(request):
    request.data['MyInfo'] = request.user.id
    serializer = StaffSerializer(data=request.data)
    email = request.data.get('email')
    myinfo_email = email

    # Check if the email already exists in the Staff model
    queryset = Staff.objects.filter(email=email)
    if email and queryset.exists():
        return Response({'Email': ['This email address is already associated with an existing Staff account.']}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists in the MyInfo model
    if myinfo_email and MyInfo.objects.filter(email=myinfo_email).exists():
        return Response({'User email': ['This email address is already associated with an existing User account.']}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Staff created successfully', 'user_data': request.user.first_name, 'staff': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_staff(request):
    staff_id = request.data.get('id')
    try:
        staff = Staff.objects.get(id=staff_id, MyInfo=request.user)
    except Staff.DoesNotExist:
        return Response({'error': ['Staff not found or you do not have permission to update it.']}, status=status.HTTP_404_NOT_FOUND)
    
    email = request.data.get('email')
    myinfo_email = email

    # Check if the new email is different from the current email
    if email and email != staff.email:
        # Check if the new email already exists in the Staff model
        queryset = Staff.objects.filter(email=email).exclude(pk=staff_id)
        if queryset.exists():
            return Response({'error': ['This email address is already associated with an existing Staff account.']}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists in the MyInfo model
    if myinfo_email and MyInfo.objects.filter(email=myinfo_email).exists():
        return Response({'error': ['This email address is already associated with an existing User account.']}, status=status.HTTP_400_BAD_REQUEST)


    serializer = StaffSerializer(staff, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Staff updated successfully', 'staff': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_staff(request):
    staff_id = request.data.get('id')
    try:
        staff = Staff.objects.get(id=staff_id, MyInfo=request.user)
    except Staff.DoesNotExist:
        return Response({'error': ['Staff not found or you do not have permission to update it.']}, status=status.HTTP_404_NOT_FOUND)

    staff.delete()
    return Response({'message': 'Staff deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
