from django.db import models
from contacts.models import *
from my_company.models import *


class Payments(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('PayPal', 'PayPal'),
        # Add more payment methods as needed
    ]

    name = models.CharField(max_length=255)
    purpose_of_use = models.CharField(max_length=255)
    booking_day = models.DateField()
    amount_gross = models.FloatField()
    open_amount_gross = models.FloatField()
    connections = models.CharField(max_length=255)
    start_date = models.DateField()
    dated = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.name





class Subscription(models.Model):
    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
        # Add more payment methods as needed
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    coupon = models.CharField(max_length=255)
    subscription_name = models.CharField(max_length=255)
    price = models.FloatField()
    time_frame = models.IntegerField()
    features = models.CharField(max_length=255)
    availability = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.subscription_name

