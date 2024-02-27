from django.db import models
from my_company.models import *
from my_company.CHOICES_Category import *
from orders.CURRENCY_CHOICES import *
from contacts.models import *
from invoices.models import *

class CaptureReceipt(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Unpaid', 'Unpaid'),
        ('Due', 'Due'),
        ('Enshrined', 'Enshrined'),
        ('Paid', 'Paid'),
        ('Part-paid', 'Part-paid'),
    ]

    VOUCHER_TYPE_CHOICES = [
        ('Expenditure', 'Expenditure'),
        ('Income', 'Income'),
    ]

    file = models.FileField(upload_to='media/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    voucher_type = models.CharField(max_length=15, choices=VOUCHER_TYPE_CHOICES)
    invoice_number = models.CharField(max_length=255)
    date_of_document = models.DateField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date_of_delivery = models.DateField()
    link_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='linked_receipts')
    due_date = models.DateField()
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    options = models.CharField(max_length=10, choices=[('Gross', 'Gross'), ('Net', 'Net')])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=15, choices=CURRENCY_CHOICES)
    sales_tax_percentage = models.PositiveIntegerField()
    sales_tax_accounted = models.BooleanField()
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.invoice_number



class CaptureRecurringReceipt(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Expired', 'Expired'),
    ]

    VOUCHER_TYPE_CHOICES = [
        ('Expenditure', 'Expenditure'),
        ('Income', 'Income'),
    ]

    INTERVAL_CHOICES = [
        ('7 Days', '7 Days'),
        ('14 Days', '14 Days'),
        ('Monthly', 'Monthly'),
        ('2 Months', '2 Months'),
        ('Quarterly', 'Quarterly'),
        ('Semiannual', 'Semiannual'),
        ('Yearly', 'Yearly'),
        ('2 Years', '2 Years'),
        ('3 Years', '3 Years'),
        ('4 Years', '4 Years'),
        ('5 Years', '5 Years'),
    ]


    file = models.FileField(upload_to='media/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    voucher_type = models.CharField(max_length=15, choices=VOUCHER_TYPE_CHOICES)
    invoice_number = models.CharField(max_length=255)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES)
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    first_voucher = models.DateField()
    last_voucher = models.DateField()
    due_date_in_days = models.PositiveIntegerField()
    due_date = models.DateField()
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)
    options = models.CharField(max_length=10, choices=[('Gross', 'Gross'), ('Net', 'Net')])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=50, choices=CURRENCY_CHOICES)
    sales_tax_rate = models.PositiveIntegerField()
    sales_tax_accounted = models.BooleanField()
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.invoice_number













