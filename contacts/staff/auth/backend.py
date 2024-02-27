from rest_framework import authentication
from rest_framework import exceptions
from contacts.models import Staff
import json
from django.contrib.auth.hashers import check_password


class StaffAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                request_data = json.loads(request.body)
                email = request_data.get('email')
                password = request_data.get('password')
                

                if not email or not password:
                    return None  # Return None when email or password is missing

                try:
                    staff = Staff.objects.get(email=email)
                except Staff.DoesNotExist:
                    return None  

                if check_password(password, staff.password):
                    # Only set request.user if authentication is successful
                    return (staff, None)

                raise exceptions.AuthenticationFailed('Invalid authentication credentials')

            except json.JSONDecodeError:
                pass

        return None

