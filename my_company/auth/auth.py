from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from my_company.serializers import *
from my_company.auth.auth_serializers import *
from my_company.models import MyInfo
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate,login
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes



@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def register_MyInfo(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if UserRateThrottle().allow_request(request, None):
            if serializer.is_valid():
                MyInfo = serializer.save()
                # For development purposes, auto-verify the email
                MyInfo.is_email_verified = True
                MyInfo.save()
                print(MyInfo.email, " has been auto verified ( Development )")
                # Send a message along with the response data
                response_data = {
                    "message": f"An email verification link has been sent to {MyInfo.email}. ( Auto verified for Development )",
                    "data": serializer.data
                }

                # Generate a verification token and create a verification URL
                token = default_token_generator.make_token(MyInfo)
                uid = urlsafe_base64_encode(force_bytes(MyInfo.pk))
                domain = get_current_site(request)
                verification_url = f"http://{domain}/auth/verify/{uid}/{token}/"
                print(verification_url)
                # Send the verification email
                # send_verification_email(MyInfo, verification_url)
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def email_verification(request, uidb64, token):
    if UserRateThrottle().allow_request(request, None):
        # Decode the MyInfo ID from the URL parameters
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            myinfo = MyInfo.objects.get(pk=uid)  # Use a different variable name
        except (TypeError, ValueError, OverflowError, MyInfo.DoesNotExist):
            myinfo = None

        if myinfo is not None and default_token_generator.check_token(myinfo, token):
            # Verification successful, update the MyInfo's status
            myinfo.is_email_verified = True
            myinfo.save()
            return Response({'message': 'Email verification successful'})
        else:
            return Response({'message': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Custom error response when rate limit is exceeded
        return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)


@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def resend_email_verification(request):    
    if UserRateThrottle().allow_request(request, None):

        if request.method == 'POST':
            email = request.data.get('email')

            try:
                user = MyInfo.objects.get(email=email)
            except MyInfo.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_email_verified:
                return Response({'message': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a new verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request)
            verification_url = f"http://{domain}/auth/verify/{uid}/{token}/"
            print(verification_url)            

            # Send the verification email (You should implement your email sending logic)
            # send_verification_email(user, verification_url)

            return Response({'message': 'Email verification link sent'}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)






@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def login_view(request):
    if UserRateThrottle().allow_request(request, None):
        if request.method == 'POST':
            serializer = LoginSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')

                # Authenticate the user
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    if user.is_email_verified:  # Check if the user's email is verified
                        # Log the user in
                        login(request, user)
                        # Generate JWT tokens
                        refresh = RefreshToken.for_user(user)
                        access_token = refresh.access_token
                        
                        # Convert Unix timestamps to human-readable format
                        token_expiry = datetime.fromtimestamp(access_token['exp'])
                        token_issued_at = datetime.fromtimestamp(access_token['iat'])

                        data = {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'token_expiry': token_expiry.strftime('%Y-%m-%d %H:%M:%S'),  # Token expiry in human-readable format
                            'token_issued_at': token_issued_at.strftime('%Y-%m-%d %H:%M:%S'),  # Token creation time in human-readable format
                            'Email': str(user.email),
                            'Password': str(user.password),
                            'User ID': str(user.id),
                            "message": f"Welcome , {user.first_name}. Login successful"
                        }
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Email is not verified'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def logout(request):
    if UserRateThrottle().allow_request(request, None):
        try:
            # In a JWT-based system, there's no server-side session to destroy.
            # To log out, the client should discard the access token.
            # The access token will automatically become invalid once it expires.
            
            # Optionally, you can send a message to indicate successful logout.
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({'message': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)





@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def forgot_password(request):
    if UserRateThrottle().allow_request(request, None):
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                return Response({'message': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate a password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f'http://{get_current_site(request)}/auth/reset-password/{uid}/{token}/'

            print("reset_url : ",reset_url)
            
            # # Send the password reset email
            # subject = 'Password Reset'
            # message = f'Click the following link to reset your password:\n\n{reset_url}'
            # from_email = 'your-email@example.com'  # Replace with your email address
            # recipient_list = [email]
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            return Response({'message': 'Password reset email sent successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)


@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def reset_password(request, uid, token):
    if UserRateThrottle().allow_request(request, None):
        serializer = PasswordResetSerializer(data=request.data)
        
        if serializer.is_valid():
            # Decode the user ID and validate the token
            try:
                user_id = force_str(urlsafe_base64_decode(uid))  # Use force_str instead of force_text
                user = get_user_model().objects.get(pk=user_id)
                if default_token_generator.check_token(user, token):
                    # Reset the user's password
                    new_password = serializer.validated_data['new_password']
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
                pass
        
        return Response({'message': 'Invalid or expired reset URL'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Request rate limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)






@api_view(['POST'])
def refresh_token_view(request):
    if request.method == 'POST':
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                old_refresh_token = RefreshToken(refresh_token)
                access_token = str(old_refresh_token.access_token)
                
                # Generate a new refresh token
                new_refresh_token = old_refresh_token.access_token.blacklist()

                # Extract token expiry and issued at information
                token_expiry = datetime.fromtimestamp(new_refresh_token['exp'])
                token_issued_at = datetime.fromtimestamp(new_refresh_token['iat'])

                # Extract user information
                user = new_refresh_token['user']
                user_email = user.email
                user_id = user.id
                user_first_name = user.first_name

                response_data = {
                    'access_token': access_token,
                    'refresh_token': str(new_refresh_token),
                    'token_expiry': token_expiry.strftime('%Y-%m-%d %H:%M:%S'),
                    'token_issued_at': token_issued_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_email': user_email,
                    'user_id': user_id,
                    'user_first_name': user_first_name
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

