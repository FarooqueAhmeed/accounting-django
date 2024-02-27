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







@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_notes(request):
    if request.method == 'GET':
        return get_notes(request)
    elif request.method == 'POST':
        return create_note(request)
    elif request.method == 'PUT':
        return update_note(request)
    elif request.method == 'DELETE':
        return delete_note(request)
    else:
        return Response({'detail': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_notes(request):
    note_id = request.data.get('id')
    if note_id:
        try:
            note = Notes.objects.get(id=note_id, MyInfo=request.user)
            serializer = NotesSerializer(note)
            response_data = {
            'message': 'Note retrieved successfully',
            'user_data': request.user.first_name, 
            'note': serializer.data,
                }
            return Response(response_data)
        except Notes.DoesNotExist:
            return Response({'detail': 'Note not found or you do not have permission to access it.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Get all notes belonging to the authenticated user
        notes = Notes.objects.filter(MyInfo=request.user)
        serializer = NotesSerializer(notes, many=True)
        response_data = {
            'message': 'Note retrieved successfully',
            'user': request.user.first_name, 
            'note': serializer.data,
                }
        response_data['note'] = []
        for note in serializer.data:
            note['MyInfo'] = request.user.first_name
            response_data['note'].append(note)

        return Response(response_data)



def send_email_to_staff(staff_emails, created_by):
  """Sends an email to the specified staff members.

  Args:
    staff_emails: A list of email addresses to send the email to.
    created_by: The name of the user who created the note.
  """

  if staff_emails:
    # for email in staff_emails:
    #   django.core.mail.send_mail(
    #     subject='New note created',
    #     message=f'A new note has been created by {created_by}.',
    #     from_email='sender@example.com', # sender email needs to be website owner
    #     recipient_list=[email],
    #   )
    print("Sent email notification to :",staff_emails,"created by :",created_by)
  else:
       print("No email to send :",staff_emails,"created by :",created_by)



def send_email_to_staff_updated(staff_emails, created_by):
  """Sends an email to the specified staff members.

  Args:
    staff_emails: A list of email addresses to send the email to.
    created_by: The name of the user who created the note.
  """

  if staff_emails:
    # for email in staff_emails:
    #   django.core.mail.send_mail(
    #     subject='New note created',
    #     message=f'A new note has been updated by {created_by}.',
    #     from_email='sender@example.com', # sender email needs to be website owner
    #     recipient_list=[email],
    #   )
    print("Sent email notification to :",staff_emails,"created by :",created_by)
  else:
       print("No email to send :",staff_emails,"created by :",created_by)


def create_note(request):
  # Set the user to the authenticated user
  request.data['MyInfo'] = request.user.id

  # Validate that the staff objects in 'staff_for_email_notification' and 'staff' are created by the user
  staff_ids = request.data.get('staff_for_email_notification', [])
  contact_id = request.data.get('contact')
  organization_id = request.data.get('organization')

  if contact_id and organization_id:
        return Response({'detail': 'Cannot specify both a contact and an organization.'}, status=status.HTTP_400_BAD_REQUEST)

  # Check 'staff_for_email_notification'
  for id in staff_ids:
    if not Staff.objects.filter(id=id, MyInfo=request.user).exists():
      return Response({'detail': 'One or more Staff for email notification are not created by request user.'}, status=status.HTTP_400_BAD_REQUEST)

  # Check 'contact'
  if contact_id:
    if not Contact.objects.filter(id=contact_id, MyInfo=request.user).exists():
      return Response({'detail': 'The contact is not created by request user.'}, status=status.HTTP_400_BAD_REQUEST)
  else:
    if not Organization.objects.filter(id=organization_id, MyInfo=request.user).exists():
      return Response({'detail': 'The Organization is not created by request user.'}, status=status.HTTP_400_BAD_REQUEST)
      

  # Get the email addresses of the staff members to notify
  staff_emails = Staff.objects.filter(id__in=staff_ids).values_list('email', flat=True)

  # Send an email to the staff members
  send_email_to_staff(staff_emails, created_by=request.user.first_name)

  # Instantiate the serializer
  serializer = NotesSerializer(data=request.data)

  # Save the note if the serializer is valid
  if serializer.is_valid():
    serializer.save()

    response_data = {
      'message': 'Note created successfully',
      'note': serializer.data,
    }

    # Replace the `staff_for_email_notification` IDs in the `note` field with the corresponding email addresses
    response_data['note']['staff_for_email_notification'] = staff_emails
    response_data['note']['MyInfo'] = request.user.first_name
    try:
        # Get the contact's first name
        contact = Contact.objects.get(id=contact_id)
        contact_first_name = contact.first_name
        response_data['note']['contact'] = contact_first_name
    except:
        pass

    try:
        # Get the Organization's name
        organization = Organization.objects.get(id=organization_id)
        organization_name = organization.organization_name
        response_data['note']['organization'] = organization_name
    except:
        pass
    # Add a message to the response if emails were sent
    if staff_emails:
      response_data['emails_sent_message'] = f'{len(staff_emails)} emails sent.'

    return Response(response_data, status=status.HTTP_201_CREATED)

  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





def update_note(request):
  note_id = request.data.get('id')
  note = get_object_or_404(Notes, id=note_id, MyInfo=request.user)  # Ensure note belongs to the user
  
  # Make sure the request user is the owner of the note
  if note.MyInfo != request.user:
        return Response({'detail': 'You are not authorized to update this note.'}, status=status.HTTP_403_FORBIDDEN)
  # Validate that the staff objects in 'staff_for_email_notification' are created by the user
  staff_ids = request.data.get('staff_for_email_notification', [])
  contact_id = request.data.get('contact')
  organization_id = request.data.get('organization')

  if contact_id and organization_id:
    return Response({'detail': 'Cannot specify both a contact and an organization.'}, status=status.HTTP_400_BAD_REQUEST)

  # Check 'staff_for_email_notification'
  for id in staff_ids:
    if not Staff.objects.filter(id=id, MyInfo=request.user).exists():
      return Response({'detail': 'One or more Staff for email notification are not created by request user.'}, status=status.HTTP_400_BAD_REQUEST)

  # Check 'contact'
  if contact_id:
    if not Contact.objects.filter(id=contact_id, MyInfo=request.user).exists():
      return Response({'detail': 'The contact is not created by request user.'}, status=status.HTTP_400_BAD_REQUEST)
  elif organization_id:
    if not Organization.objects.filter(id=organization_id, MyInfo=request.user).exists():
      return Response({'detail': 'The Organization is not created by request user.'}, status=status.HTTP_400_BAD_REQUEST)

  # Get the email addresses of the staff members to notify
  staff_emails = Staff.objects.filter(id__in=staff_ids).values_list('email', flat=True)

  # Send an email to the staff members
  send_email_to_staff_updated(staff_emails, created_by=request.user.first_name)

  serializer = NotesSerializer(note, data=request.data, partial=True)  # Use partial update
  if serializer.is_valid():
    updated_note = serializer.save()
    

    # After saving the note, fetch the updated staff names for the response
    updated_staff_names = list(updated_note.staff_for_email_notification.values_list('name', flat=True))

    response_data = {
      'message': 'Note updated successfully',
      'note': serializer.data,
    }
    # Replace the `staff_for_email_notification` IDs in the `note` field with the corresponding staff names
    response_data['note']['staff_for_email_notification'] = updated_staff_names
    # Replace the `staff_for_email_notification` IDs in the `note` field with the corresponding staff names
    #response_data['note']['staff_for_email_notification'] = list(staff_emails)

    # Add additional information from related models if needed
    response_data['note']['organization_name'] = updated_note.organization.organization_name if updated_note.organization else None
    response_data['note']['contact_first_name'] = updated_note.contact.first_name if updated_note.contact else None
    response_data['note']['MyInfo'] = request.user.first_name

    # Add a message to the response if emails were sent
    if staff_emails:
      response_data['emails_sent_message'] = f'{len(staff_emails)} emails sent.'

    return Response(response_data, status=status.HTTP_200_OK)

  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def delete_note(request):
    note_id = request.data.get('id')
    note = get_object_or_404(Notes, id=note_id)
    # Ensure that the user is the owner of the note
    if note.MyInfo != request.user:
        return Response({'detail': 'You do not have permission to delete this note.'}, status=status.HTTP_403_FORBIDDEN)

    note.delete()
    response_data = {
      'message': 'Note deleted successfully',
    }
    return Response(response_data,status=status.HTTP_204_NO_CONTENT)





