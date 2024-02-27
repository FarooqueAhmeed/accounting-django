from django.db import models
from my_company.models import *
from my_company.choices_LANGUAGES_COUNTRIES import *
from products.models import *
from datetime import timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import datetime



class Organization(models.Model):
    organization_name = models.CharField(max_length=255, null=False)
    name_suffix = models.CharField(max_length=255, null=False)
    customer_number = models.CharField(max_length=255, null=False)
    debtor_number = models.PositiveIntegerField(null=False)

    contact_type = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)
    contacts = models.ManyToManyField('Contact',blank=True, related_name='organization_contacts')  # Use 'Contact' in quotes since it's defined later in the same module
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved

    def __str__(self):
        return self.organization_name

class Contact(models.Model):
    SALUTATION_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Miss', 'Miss'),
        ('Other', 'Other'),
    ]

    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, null=False)
    title = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    legal_name = models.CharField(max_length=255, null=False)
    customer_number = models.CharField(max_length=255, null=False)
    line_item = models.CharField(max_length=255, null=False)
    debtor_number = models.PositiveIntegerField(null=False)
    contact_type = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True, blank=True, related_name='contact_organizations') 
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)  

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class AddressForContact(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('work', 'Work'),
        ('private', 'Private'),
        ('invoice', 'Invoice Address'),
        ('delivery', 'Delivery Address'),
        ('collection', 'Collection Address'),
    )

    street = models.CharField(max_length=255, null=True, blank=True)
    ZIP_code = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, choices=COUNTRIES_CHOICES, null=True, blank=True)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return f"{self.street}, {self.ZIP_code}, {self.city}, {self.country}"



class ContactDetailsForContact(models.Model):
    CONTACT_CHOICES = (
        ('work', 'Work'),
        ('autobox', 'Autobox'),
        ('fax', 'Fax'),
        ('mobile', 'Mobile'),
        ('newsletter', 'Newsletter'),
        ('private', 'Private'),
        ('invoice_address', 'Invoice Address'),
    )

    phone = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)
    phone_type = models.CharField(max_length=255, choices=CONTACT_CHOICES, null=True, blank=True)
    email_type = models.CharField(max_length=255, choices=CONTACT_CHOICES, null=True, blank=True)
    web_url_type = models.CharField(max_length=255, choices=CONTACT_CHOICES, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return f"{self.phone} - {self.email} - {self.web_url}"


class PaymentInformationForContacts(models.Model):
    routing_number = models.PositiveIntegerField(null=True, blank=True)
    swift_code = models.PositiveIntegerField(null=True, blank=True)
    sales_tax_id = models.PositiveIntegerField(null=True, blank=True)
    tax_reference = models.CharField(max_length=255,null=True, blank=True)
    show_vat_id = models.BooleanField(default=False,null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return f"Routing: {self.routing_number}, Swift: {self.swift_code}, Sales Tax ID: {self.sales_tax_id}, Tax Reference: {self.tax_reference}, Show VAT ID: {self.show_vat_id}"


class ConditionsForContacts(models.Model):
    cash_discount_days = models.PositiveIntegerField(null=True, blank=True)
    cash_discount_percent = models.PositiveIntegerField(null=True, blank=True)
    payment_due_days = models.PositiveIntegerField(null=True, blank=True)
    
    CUSTOMER_DISCOUNT_CHOICES = [
        ('%', '%'),
        ('EUR', 'EUR'),
    ]
    customer_discount_type = models.CharField(max_length=3, choices=CUSTOMER_DISCOUNT_CHOICES,null=True, blank=True)
    customer_discount_value = models.PositiveIntegerField(null=True, blank=True)

    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        return f"Cash Discount Days: {self.cash_discount_days}, Cash Discount Percent: {self.cash_discount_percent}%, Payment Due Days: {self.payment_due_days}, Customer Discount: {self.customer_discount_type}"



class AdditionalInformation(models.Model):
    tags = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    birthday = models.DateField(null=True, blank=True)  #only for contact
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True, blank=True) 

    def __str__(self):
        if self.organization:
            return f'Additional Info for Organization: {self.organization}'
        elif self.contact:
            return f'Additional Info for Contact: {self.contact}'
        else:
            return 'Additional Information'



class Notes(models.Model):
    note = models.CharField(max_length=255,null=False, blank=False)
    staff_for_email_notification = models.ManyToManyField(Staff, blank=True, related_name='staff_for_email')
    date_of_notice = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='media/', null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,null=True, blank=True, related_name='contact_related') 
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved

    def __str__(self):
        return self.note


STATUS_CHOICES = [
    ('Draft', 'Draft'),
    ('Sent', 'Sent'),
    ('Pending', 'Pending'),
]

SEND_AS_CHOICES = [
    ('Print', 'Print'),
    ('Email', 'Email'),
    ('WhatsApp', 'WhatsApp'),
]

class Letters(models.Model):
    internal_contact_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='internal_contact', null=True, blank=True)
    contact_receiver = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='letters_receiver', null=True, blank=True)
    date = models.DateField(default=datetime.now, blank=False, null=False)
    your_signature = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=355, blank=False, null=False,default="default")
    subject = models.CharField(max_length=255, blank=False, null=False)
    country = models.CharField(max_length=30,choices=COUNTRIES_CHOICES,blank=False, null=False, default='AUT')
    text = models.TextField(max_length=1000, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    send_as = models.CharField(max_length=20, choices=SEND_AS_CHOICES, default='Email')
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name='related_organization', null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='related_contact', null=True, blank=True)


    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    
    def __str__(self):
        receiver_name = self.contact_receiver.first_name if self.contact_receiver else "Unknown Receiver"
        return f"Letter to {receiver_name} on {self.date.strftime('%Y-%m-%d')}"


#Remaining
class CustomerPricing(models.Model):
    customer_price_net = models.DecimalField(max_digits=20, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved

    def __str__(self):
        return f"Customer Pricing for {self.contact} - {self.product}"



class Task(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    days = models.PositiveIntegerField(blank=False, null=False,default=0)
    due_date = models.DateField(blank=False, null=False,default=timezone.now)
    assignee = models.ForeignKey(Staff, on_delete=models.CASCADE , null=True, blank=True)
    TASK_TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('none', 'None'),
        ('appointment', 'Appointment'),
        ('estimate', 'Estimate'),
        ('fax', 'Fax'),
    ]
    type_of_task = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, blank=False, null=False)
    notify_when_done = models.BooleanField(default=False, blank=False, null=False)
    completed = models.BooleanField(default=False, null=True,blank=True)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    
    def save(self, *args, **kwargs):
        # Automatically set the Due Date based on the provided number of days
        if self.days and self.due_date:
            # Automatically set the Due Date based on the provided number of days
            self.due_date = self.due_date + timedelta(days=self.days)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description










