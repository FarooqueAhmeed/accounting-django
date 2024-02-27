from django.core.exceptions import ValidationError
from my_company.models import MyInfo 
import re
from rest_framework import serializers
from django.core.mail import send_mail

def send_verification_email(MyInfo, verification_url):
    subject = "Email Verification"
    message = f"Click the following link to verify your email: {verification_url}"
    from_email = 'your@email.com'  # Set your email address
    recipient_list = [MyInfo.email]
    
    send_mail(subject, message, from_email, recipient_list)
