from django.db import models
from my_company.models import *
from my_company.choices_LANGUAGES_COUNTRIES import *
from products.models import *
from contacts.models import *
from orders.CURRENCY_CHOICES import *


class TotalDiscount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('discount', 'Discount'),
        ('surcharge', 'Surcharge'),
    ]

    DISCOUNT_CHOICES = [
        ('%', '%'),
        ('euro', 'Euro'),
    ]

    type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    discount = models.CharField(max_length=10, choices=DISCOUNT_CHOICES)
    value = models.PositiveIntegerField()
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f'{self.get_type_display()}: {self.description}'



class LineItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField()
    
    QUANTITY_TYPE_CHOICES = [
        ('unit', 'Unit'),
        ('flat-rate', 'Flat-rate'),
        ('hour(s)', 'Hour(s)'),
        ('%', '%'),
        ('day(s)', 'Day(s)'),
        ('inch', 'Inch'),
        ('foot', 'Foot'),
        ('yd', 'Yard'),
        ('mile(s)', 'Mile(s)'),
        ('yd²', 'Yard²'),
        ('yd³', 'Yard³'),
        ('oz', 'Ounce'),
        ('gal', 'Gallon'),
    ]
    quantity_type = models.CharField(max_length=20, choices=QUANTITY_TYPE_CHOICES)
    
    single_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    SINGLE_PRICE_CHOICES = [
        ('net', 'Net'),
        ('gross', 'Gross'),
    ]
    single_price_type = models.CharField(max_length=5, choices=SINGLE_PRICE_CHOICES)
    
    sales_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    discount = models.PositiveIntegerField()
    
    DISCOUNT_TYPE_CHOICES = [
        ('%', '%'),
        ('EUR', 'EUR'),
    ]
    discount_type = models.CharField(max_length=5, choices=DISCOUNT_TYPE_CHOICES)
    
    note = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f'Line Item for {self.product.product_name}'

class OrderCommon(models.Model):
    SUBJECT_CHOICES = [
        ('draft', 'Draft'),
        ('unpaid', 'Unpaid'),
        ('received', 'Received'),
        ('calculated', 'Calculated'),
        ('partly_calculated', 'Partly Calculated'),
        ('rejected', 'Rejected'),
        ('archive', 'Archive'),
    ]
    regarding_subject = models.CharField(max_length=255)
    reference_order_no = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=20, choices=COUNTRIES_CHOICES)
    header_text = models.CharField(max_length=255)
    foot_text = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.reference_order_no



class MoreOptionsForOrder(models.Model):

    SALES_TAX_RULE_CHOICES = [
        ('sales_tax_code', 'Identify Sales Tax Code'),
        ('intra_community_delivery', 'Tax-Free Intra-Community Delivery (EU)'),
        ('tax_obligation', 'Tax Obligation of the Beneficiary (Outside the EU, e.g. Switzerland)'),
    ]

    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES)
    delivery_terms = models.CharField(max_length=255)
    internal_contact_person = models.ForeignKey(Contact, on_delete=models.CASCADE)
    payment_terms = models.CharField(max_length=255)
    sales_tax_rule = models.CharField(max_length=50, choices=SALES_TAX_RULE_CHOICES)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f"Order Options - {self.currency}"



class Estimates(models.Model):
    estimate_number = models.CharField(max_length=255)
    estimate_date = models.DateTimeField()
    reference_estimate_number = models.CharField(max_length=255)
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE) 
    discounts = models.ForeignKey(TotalDiscount, on_delete=models.CASCADE)  
    more_options_for_order = models.ForeignKey(MoreOptionsForOrder, on_delete=models.CASCADE)  
    order_common = models.ForeignKey(OrderCommon, on_delete=models.CASCADE)  
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)  
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.estimate_number


class DeliveryNotes(models.Model):
    delivery_note_number = models.CharField(max_length=255)
    delivery_note_date = models.DateField()
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE) 
    discounts = models.ForeignKey(TotalDiscount, on_delete=models.CASCADE)  
    more_options_for_order = models.ForeignKey(MoreOptionsForOrder, on_delete=models.CASCADE)  
    order_common = models.ForeignKey(OrderCommon, on_delete=models.CASCADE)  
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)  
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.delivery_note_number


class OrderConfirmations(models.Model):
    order_number = models.CharField(max_length=255)
    order_date = models.DateTimeField()
    reference_order_no = models.CharField(max_length=255)
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE)  
    total_discount = models.ForeignKey(TotalDiscount, on_delete=models.CASCADE) 
    more_options_for_order = models.ForeignKey(MoreOptionsForOrder, on_delete=models.CASCADE) 
    order_common = models.ForeignKey(OrderCommon, on_delete=models.CASCADE)  
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)  
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.order_number
















