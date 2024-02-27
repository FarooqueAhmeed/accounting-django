from django.db import models
from my_company.models import *
from my_company.choices_LANGUAGES_COUNTRIES import *



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('article', 'Article'),
        ('service', 'Service'),
    ]

    STANDARD_UNIT_CHOICES = [
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

    product_name = models.CharField(max_length=255)
    product_no = models.PositiveIntegerField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    sales_tax_rate = models.PositiveIntegerField()
    standard_unit = models.CharField(max_length=20, choices=STANDARD_UNIT_CHOICES)
    stock_unit = models.CharField(max_length=20, blank=True)  # Set the stock_unit based on the selected standard_unit
    purchase_price_net = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price_gross = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price_net = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price_gross = models.DecimalField(max_digits=10, decimal_places=2)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.product_name


class ProductDescription(models.Model):
    product_description = models.CharField(max_length=255)
    internal_comment = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.product_description


class ProductMoreUnits(models.Model):
    UNIT_CHOICES = [
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

    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    factor = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #(this is value , this needs to be created auto from , unit x factor = price)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.product.product_name
    



class ProductMoreSettings(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_enabled = models.BooleanField(default=False)
    reorder_notification = models.BooleanField(default=False)
    threshold_level = models.FloatField(null=True, blank=True)
    REMIND_ME_CHOICES = [
        ('Daily', 'Daily'),
        ('2 days', '2 days'),
        ('3 days', '3 days'),
        ('4 days', '4 days'),
        ('5 days', '5 days'),
        ('6 days', '6 days'),
        ('7 days', '7 days'),
    ]

    remind_me = models.CharField(max_length=10, choices=REMIND_ME_CHOICES, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f'Settings for {self.product.product_name}'

    def save(self, *args, **kwargs):
        # Enable/disable fields based on conditions
        if self.stock_enabled:
            self.reorder_notification = True

        if self.stock_enabled and self.reorder_notification:
            self.threshold_level = 0.0
            self.remind_me = 'Daily'
        else:
            self.threshold_level = None
            self.remind_me = None

        super().save(*args, **kwargs)



















