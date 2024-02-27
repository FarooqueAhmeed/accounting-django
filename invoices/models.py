from django.db import models
from orders.CURRENCY_CHOICES import *
from contacts.models import *
from orders.models import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


class CostCenter(models.Model):
    name = models.CharField(max_length=255)
    number = models.PositiveIntegerField()
    color_code = models.CharField(max_length=10)
    cross_company_code = models.PositiveIntegerField()
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)  
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.name



class MoreOptionsForInvoice(models.Model):
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    days_for_cash_discount = models.PositiveIntegerField()
    percentage_for_cash_discount = models.FloatField()
    internal_contact_person = models.ForeignKey(Contact, on_delete=models.CASCADE)
    
    PAYMENT_METHOD_CHOICES = [
        ('no_default', 'No Default'),
        ('sepa_transfer', 'SEPA Transfer'),
        ('sepa_direct_debit', 'SEPA Direct Debit'),
        ('cash', 'Cash'),
        ('debt_settlement', 'Debt Settlement Between Both Parties'),
        ('check', 'Check'),
    ]
    payment_methods = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
    
    SALES_TAX_RULE_CHOICES = [
        ('identify_tax_code', 'Identify Sales Tax Code'),
        ('tax_free_intra_community', 'Tax-Free Intra-Community Delivery (EU)'),
        ('tax_obligation_beneficiary', 'Tax Obligation of the Beneficiary (Outside the EU, e.g. Switzerland)'),
    ]
    sales_tax_rule = models.CharField(max_length=50, choices=SALES_TAX_RULE_CHOICES)

    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f"More Options for Invoice - {self.currency}"


# Define a custom validation function for 'duration_time'
def validate_duration_time(value):
    # Use a regular expression to ensure the format is 'from - to'
    if not re.match(r'^\d{2}:\d{2} - \d{2}:\d{2}$', value):
        raise ValidationError('Invalid format. Use "hh:mm - hh:mm" format.')

# Define a custom validation function for 'duration_hour'
def validate_duration_hour(value):
    # Use a regular expression to ensure the format is 'hh:mm'
    if not re.match(r'^\d{2}:\d{2}$', value):
        raise ValidationError('Invalid format. Use "hh:mm" format.')

class TimeTracking(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    project = models.CharField(max_length=255)
    employee = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='employee_time_tracking')
    duration_time = models.CharField(max_length=20, validators=[validate_duration_time], help_text="Use 'hh:mm - hh:mm' format")
    duration_hour = models.CharField(max_length=5, validators=[validate_duration_hour], help_text="Use 'hh:mm' format")
    date = models.DateField()
    task_service = models.ForeignKey(Task, on_delete=models.CASCADE)
    hourly_rate_net = models.FloatField()
    sales_tax_rate = models.PositiveIntegerField()
    is_billable = models.BooleanField()
    description = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f"Time Tracking for {self.contact} on {self.date}"



class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Unpaid', 'Unpaid'),
        ('Due', 'Due'),
        ('Paid', 'Paid'),
        ('Part-Paid', 'Part-Paid'),
        ('Reversal', 'Reversal'),
        ('Enshrined', 'Enshrined'),
        ('Recurring', 'Recurring'),
    ]

    invoice_header = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=20)
    invoice_date = models.DateField()
    due_date_days = models.PositiveIntegerField(blank=True, null=True)
    due_date_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    time_tracking = models.ForeignKey(TimeTracking, on_delete=models.CASCADE)
    total_discount = models.ForeignKey(TotalDiscount, on_delete=models.CASCADE)
    more_options = models.ForeignKey(MoreOptionsForInvoice, on_delete=models.CASCADE)
    order_common = models.ForeignKey(OrderCommon, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def save(self, *args, **kwargs):
        # Automatically set the due date based on due_date_days or due_date_date
        if self.due_date_days:
            self.due_date_date = self.invoice_date + timedelta(days=self.due_date_days)
        elif self.due_date_date:
            self.due_date_days = (self.due_date_date - self.invoice_date).days

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number



class RecurringInvoice(models.Model):
    INVOICE_INTERVAL_CHOICES = [
        ('7 Days', '7 Days'),
        ('14 Days', '14 Days'),
        ('Monthly', 'Monthly'),
        ('2 Months', '2 Months'),
        ('Quarterly', 'Quarterly'),
        ('Semi-Annual', 'Semi-Annual'),
        ('Yearly', 'Yearly'),
        ('2 Years', '2 Years'),
        ('3 Years', '3 Years'),
        ('4 Years', '4 Years'),
        ('5 Years', '5 Years'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Ready / Due', 'Ready / Due'),
    ]

    automatic_invoice_generation = models.BooleanField()
    invoice_header = models.CharField(max_length=255)
    first_invoice = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    invoice_interval = models.CharField(max_length=15, choices=INVOICE_INTERVAL_CHOICES)
    postpone = models.BooleanField()
    due_date_in_days = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    time_tracking = models.ForeignKey(TimeTracking, on_delete=models.CASCADE)
    total_discount = models.ForeignKey(TotalDiscount, on_delete=models.CASCADE)
    more_options = models.ForeignKey(MoreOptionsForInvoice, on_delete=models.CASCADE)
    order_common = models.ForeignKey(OrderCommon, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def save(self, *args, **kwargs):
        # Automatically update the due date if the status is "Ready / Due"
        if self.status == 'Ready / Due':
            self.due_date_in_days = (self.first_invoice - self.end_date).days

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_header
















