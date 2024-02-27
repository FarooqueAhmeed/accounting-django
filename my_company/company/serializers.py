from rest_framework import serializers
from my_company.models import *
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator



class MyCompanyAddressSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    legal_company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    company_holder = serializers.CharField(max_length=255, required=False, allow_blank=True)
    type_of_company = serializers.ChoiceField(choices=COMPANY_TYPE_CHOICES, required=False, allow_blank=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    zip_code = serializers.IntegerField(required=False)
    city = serializers.CharField(max_length=255, required=False, allow_blank=True)
    country = serializers.ChoiceField(choices=COUNTRIES_CHOICES, required=False, allow_blank=True)
    industry = serializers.CharField(max_length=255, required=False, allow_blank=True)
    number_of_coworkers = serializers.ChoiceField(choices=CO_WORKERS_CHOICES, required=False, allow_blank=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=MyInfo.objects.all(), required=False)

    class Meta:
        model = MyCompanyAddress
        fields = '__all__'

    # Add custom validation for the zip_code field
    def validate_zip_code(self, value):
        if value is not None:
            if not str(value).isnumeric():
                raise serializers.ValidationError('Zip code must be a numeric value.')
            if len(str(value)) != 5:
                raise serializers.ValidationError('Zip code must be exactly 5 digits.')

        return value

class MyCompanyTaxInfoSerializer(serializers.ModelSerializer):
    district_court = serializers.CharField(max_length=255, required=False)
    corporation_registration_number = serializers.CharField(max_length=255, required=False)
    sales_tax_id = serializers.IntegerField(required=False)
    tax_reference = serializers.CharField(max_length=255, required=False)
    tax_rate = serializers.IntegerField(required=False)
    cash_basis_on_payment_date = serializers.BooleanField(required=False)
    accounting_method = serializers.ChoiceField(
        choices=MyCompanyTaxInfo.ACCOUNTING_METHOD_CHOICES,
        required=False
    )
    income_statement_method = serializers.ChoiceField(
        choices=MyCompanyTaxInfo.INCOME_STATEMENT_METHOD_CHOICES,
        required=False
    )
    prices_on_documents = serializers.ChoiceField(
        choices=MyCompanyTaxInfo.PRICES_ON_DOCUMENTS_CHOICES,
        required=False
    )

    class Meta:
        model = MyCompanyTaxInfo
        fields = '__all__'





class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

    def validate_name(self, value):
        # Check if the 'name' field is required
        if not value:
            raise serializers.ValidationError("Name is required.")
        # You can add min and max length validations if needed
        min_length = 2
        max_length = 255
        if len(value) < min_length or len(value) > max_length:
            raise serializers.ValidationError(f"Name must be between {min_length} and {max_length} characters.")

        return value

    def validate_my_info(self, value):
        # Check if the 'my_info' field is required
        if value is None:
            raise serializers.ValidationError("User is required.")
        return value




class MyCompanyContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCompanyContactInfo
        fields = '__all__'

    def validate_phone(self, value):
        if len(value) > 20:
            raise serializers.ValidationError('Phone number should not exceed 20 characters.')
        return value

    def validate_fax(self, value):
        if value < 0:
            raise serializers.ValidationError('Fax number should be a positive integer.')
        return value

    def validate_email(self, value):
        if value and len(value) > 254:
            raise serializers.ValidationError('Email address should not exceed 254 characters.')
        return value

    def validate_web(self, value):
        if value and len(value) > 2000:
            raise serializers.ValidationError('Web URL should not exceed 2000 characters.')
        return value


class MyCompanyPaymentInfoSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(max_length=255, required=False, validators=[RegexValidator(regex=r'^[A-Za-z\s]+$', message="Bank name should contain only letters.")])
    account_number = serializers.CharField(max_length=33, required=False, validators=[RegexValidator(regex=r'^[0-9]+$', message="Account number should contain only digits")])
    sort_code = serializers.IntegerField(required=False, validators=[RegexValidator(regex=r'^[0-9]+$', message="Sort code should contain only digits")])
    routing_number = serializers.CharField(max_length=255, required=False, validators=[RegexValidator(regex=r'^[0-9]+$', message="Routing number should contain only digits")])
    swift_code = serializers.CharField(max_length=255, required=False, validators=[RegexValidator(regex=r'^[0-9]+$', message="SWIFT code should contain only digits")])

    class Meta:
        model = MyCompanyPaymentInfo
        fields = '__all__'



def validate_logo_extension(value):
    valid_extensions = ['jpeg', 'jpg', 'png']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError(f"File type not supported. Supported extensions are: {', '.join(valid_extensions)}")


class MyCompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCompanyLogo
        fields = '__all__'  # You can specify specific fields if needed

    logo = serializers.ImageField(validators=[validate_logo_extension])
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

    

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255,required=False,validators=[RegexValidator(regex=r'^[A-Za-z\s]+$',message="Name should contain only letters and spaces."),MinLengthValidator(limit_value=3,message="Name must be at least 3 characters long."),MaxLengthValidator(limit_value=255,message="Name cannot exceed 255 characters.")])
    color = serializers.CharField(max_length=30, required=False)
    abbreviation = serializers.CharField(max_length=10,required=False,validators=[MinLengthValidator(limit_value=2,message="Abbreviation must be at least 2 characters long."),MaxLengthValidator(limit_value=10,message="Abbreviation cannot exceed 10 characters.")])
    sale_or_purchase = serializers.ChoiceField(choices=SALE_PURCHASE_CHOICES,required=False)
    overall_debtor_account = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Category
        fields = '__all__'








