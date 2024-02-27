from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from my_company.models import *
from my_company.my_info.serializers import *

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_my_info(request):
    try:
        # Retrieve the MyInfo object associated with the authenticated user
        my_info = MyInfo.objects.get(email=request.user.email)
    except MyInfo.DoesNotExist:
        return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        new_email = request.data.get('email')

        # Check if the user is attempting to update their own data
        if my_info != request.user:
            return Response({'error': 'You do not have permission to update this user\'s data.'}, status=status.HTTP_403_FORBIDDEN)

        if new_email:
            if new_email != request.user.email:  # Check if the new email is different from the current email
                # Check if the new email is associated with another user
                conflicting_user = MyInfo.objects.filter(email=new_email).exclude(pk=my_info.pk).first()
                if conflicting_user:
                    return Response({'error': 'Email is already associated with another user!!!!.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    print(f"No conflict: {new_email} is the same as the current user's email.")

        serializer = MyInfoUpdateSerializer(my_info, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Include a custom message in the response
            response_data = {
                'message': f'We have updated your profile, {my_info.first_name}.',
                'data': serializer.data
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user  # The authenticated user

    if user:
        # Serialize the user's data
        serializer = MyInfoSerializer(user)

        response_data = {
            'message': 'User information fetched successfully.',
            'data': serializer.data
        }

        return Response(response_data)
    else:
        return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_my_info(request):
    user = request.user  
    try:
        my_info = MyInfo.objects.get(id=user.id)
    except MyInfo.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        my_info.delete()
        return Response({'message': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
