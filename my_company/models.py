from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from my_company.choices_LANGUAGES_COUNTRIES import *
from my_company.CHOICES_Category import *
from my_company.country_codes import *
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class MyInfo(AbstractBaseUser, PermissionsMixin):    
    SALUTATION_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Miss', 'Miss'),
        ('Other', 'Other'),
    ]


    email = models.EmailField(unique=True, error_messages={'unique': 'This email address is already associated with an existing account'})
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5, choices=COUNTRY_CODES_CHOICES, default='+1')  
    company_headquarters = models.CharField(max_length=3, choices=COUNTRIES_CHOICES)
    language = models.CharField(max_length=3, choices=LANGUAGES_CHOICES)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)

    salutation = models.CharField(max_length=8,choices=SALUTATION_CHOICES,default='Mr.',null=True, blank=True )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
      # Add related_name attributes to resolve clashes
    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='myinfo_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, related_name='myinfo_user_permissions')

    def save(self, *args, **kwargs):
        if not self.abbreviation:
            # Auto-generate the abbreviation based on the first name
            self.abbreviation = slugify(self.first_name)[:10]
        super(MyInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.email




# Choices for Type of category
CATEGORY_TYPE_CHOICES = [
    ('contact', 'Contact'),
    ('product', 'Product'),
    ('task', 'Task'),
]

# Choices for Type of category (Sale or Purchase)
SALE_PURCHASE_CHOICES = [
    ('sale', 'Sale (e.g., customer, prospect)'),
    ('purchase', 'Purchase (e.g., supplier)'),
]

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)  # CharField for storing color as a character string
    abbreviation = models.CharField(max_length=10, blank=True, null=True)
    sale_or_purchase = models.CharField(max_length=20, choices=SALE_PURCHASE_CHOICES, blank=True, null=True)
    overall_debtor_account = models.CharField(max_length=255, blank=True, null=True)
    my_info = models.ForeignKey('MyInfo',on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def save(self, *args, **kwargs):
        if not self.abbreviation:
            # Auto-generate the abbreviation based on the name
            self.abbreviation = slugify(self.name)[:10]
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name





# Choices for Type of company
COMPANY_TYPE_CHOICES = [
    ('self-employed', 'Self-Employed'),
    ('sole-proprietor', 'Sole Proprietor'),
    ('business-partnership', 'Business Partnership'),
    ('nonprofit', 'Nonprofit'),
    ('private-business-partnership', 'Private Business Partnership'),
    ('incorporated-company', 'Incorporated Company'),
]

# Choices for Number of co-workers
CO_WORKERS_CHOICES = [
    ('only-me', 'Only Me'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('more-than-10', 'More than 10'),
]

class MyCompanyAddress(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    legal_company_name = models.CharField(max_length=255, null=True, blank=True)
    company_holder = models.CharField(max_length=255, null=True, blank=True)
    type_of_company = models.CharField(max_length=30, choices=COMPANY_TYPE_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=20, choices=COUNTRIES_CHOICES, null=True, blank=True)
    industry = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)  
    number_of_coworkers = models.CharField(max_length=20, choices=CO_WORKERS_CHOICES, null=True, blank=True)
    owner = models.ForeignKey('MyInfo', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.company_name





class MyCompanyTaxInfo(models.Model):
    district_court = models.CharField(max_length=255, default="Default District Court", null=True, blank=True)
    corporation_registration_number = models.CharField(max_length=255, default="Default Registration Number", null=True, blank=True)
    sales_tax_id = models.IntegerField(default=0, null=True, blank=True)  # You can specify a default integer value
    tax_reference = models.CharField(max_length=255, default="Default Tax Reference", null=True, blank=True)
    tax_rate = models.IntegerField(default=0, null=True, blank=True)  # Specify the default integer value
    cash_basis_on_payment_date = models.BooleanField(default=False, null=True, blank=True)  # Specify the default boolean value
    
    ACCOUNTING_METHOD_CHOICES = [
        ('Cash basis', 'Cash basis'),
        ('Standard accounting system 04', 'Standard accounting system 04'),
        ('Standard accounting system austria', 'Standard accounting system austria'),
    ]
    accounting_method = models.CharField(max_length=255, choices=ACCOUNTING_METHOD_CHOICES, default="Cash basis", null=True, blank=True)  # Specify the default choice
    
    INCOME_STATEMENT_METHOD_CHOICES = [
        ('Income STMT', 'Income STMT'),
        ('Profit and loss', 'Profit and loss'),
    ]
    income_statement_method = models.CharField(max_length=255, choices=INCOME_STATEMENT_METHOD_CHOICES, default="Income STMT", null=True, blank=True)  # Specify the default choice
    
    PRICES_ON_DOCUMENTS_CHOICES = [
        ('Without VAT', 'Price on documents are without VAT'),
        ('Include VAT', 'Price on documents include VAT'),
    ]
    prices_on_documents = models.CharField(max_length=255, choices=PRICES_ON_DOCUMENTS_CHOICES, default="Without VAT", null=True, blank=True)  # Specify the default choice
    
    my_company_address = models.ForeignKey('MyCompanyAddress', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.district_court


class Tags(models.Model):
    name = models.CharField(max_length=255)
    my_info = models.ForeignKey('MyInfo',on_delete=models.CASCADE, null=True, blank=True) 
    def __str__(self):
        return self.name

class MyCompanyContactInfo(models.Model):
    phone = models.CharField(null=True, blank=True,max_length=20)
    fax = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    web = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tags)    
    my_company_address = models.ForeignKey('MyCompanyAddress', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.phone


class MyCompanyPaymentInfo(models.Model):
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.PositiveIntegerField(null=True, blank=True)
    sort_code = models.PositiveIntegerField()
    routing_number = models.CharField(max_length=255, null=True, blank=True)
    swift_code = models.PositiveIntegerField(null=True, blank=True)
    
    my_company_address = models.ForeignKey('MyCompanyAddress', on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return self.bank_name


class MyCompanyLogo(models.Model):
    # Link the logo to a specific MyCompanyAddress instance
    company_address = models.OneToOneField('MyCompanyAddress', on_delete=models.CASCADE, related_name='logo', null=True, blank=True)

    # Field to store the logo image
    logo = models.ImageField(upload_to='media/')  # You can specify the path where logos will be stored
    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    def __str__(self):
        return f"Logo for {self.company_address.company_name}"

class Staff(models.Model):
    MyInfo_TYPES = [
        ('administrator', 'Administrator'),
        ('auditor', 'Auditor'),
        ('staff', 'Staff'),
    ]

    SALUTATION_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Miss', 'Miss'),
        ('Other', 'Other'),
    ]


    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=300, blank=False, null=False,default="")
    user_type = models.CharField(max_length=15, choices=MyInfo_TYPES,blank=False, null=False)
    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES,blank=False, null=False)
    language = models.CharField(max_length=10, choices=LANGUAGES_CHOICES,blank=False, null=False)
    abbreviation = models.CharField(max_length=10, blank=True, null=True)  # We'll generate this based on the name
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate abbreviation from the name
        self.abbreviation = slugify(self.name)[:5]
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Extensions(models.Model):
    EXTENSION_TYPES = [
        ('Type1', 'Type 1'),
        ('Type2', 'Type 2'),
        ('Type3', 'Type 3'),
        # Add more extension types as needed
    ]

    name = models.CharField(max_length=255)
    extension_type = models.CharField(max_length=20, choices=EXTENSION_TYPES)
    connected = models.BooleanField()
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class API(models.Model):
    token = models.CharField(max_length=255)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.token


