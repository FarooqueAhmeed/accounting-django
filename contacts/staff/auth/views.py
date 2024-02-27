from rest_framework.decorators import api_view, authentication_classes, throttle_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .backend import *
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import login
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
import json



@api_view(['POST'])
@authentication_classes([StaffAuthentication]) 
def login_staff(request):
    if request.content_type == 'application/json':
        staff = request.user  # This will be the authenticated Staff instance returned by your custom authentication

        if staff is not None:
            request_data = json.loads(request.body)
            email = request_data.get('email')
            password = request_data.get('password')

            if not email or not password:
                return Response({'error': 'Email and password are required.'}, status=400)
                        
           # Validate if staff.email exists
            try:
                Staff.objects.get(email=email)
            except Staff.DoesNotExist:
                return Response({'error': 'Invalid authentication credentials.'}, status=404)
            
            if staff.email != email:
                return Response({'error': 'Email does not match the authenticated user.'}, status=403)

            
            if check_password(password, staff.password):
                # Log in the staff
                login(request, staff, backend='django.contrib.auth.backends.ModelBackend')

                # Generate JWT tokens
                refresh = RefreshToken.for_user(staff)
                access_token = refresh.access_token

                # Convert Unix timestamps to human-readable format
                token_expiry = refresh.access_token['exp']
                token_issued_at = refresh.access_token['iat']

                data = {
                    'refresh': str(refresh),
                    'access': str(access_token),
                    'token_expiry': token_expiry,
                    'token_issued_at': token_issued_at,
                    'Email': staff.email,
                    'User type': staff.user_type,
                    # Add other staff-related data here
                    'message': f'Welcome, {staff.email}. Login successful'
                }

                return Response(data, status=200)

            return Response({'error': 'Invalid password.'}, status=403)

        return Response({'error': 'Invalid authentication credentials.'}, status=403)

    return Response({'error': 'Invalid request format.'}, status=400)
