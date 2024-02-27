from rest_framework import serializers
from contacts.models import *
from my_company.choices_LANGUAGES_COUNTRIES import *


ADDRESS_TYPE_CHOICES = (
        ('work', 'Work'),
        ('private', 'Private'),
        ('invoice', 'Invoice Address'),
        ('delivery', 'Delivery Address'),
        ('collection', 'Collection Address'),
    )

class AddressForContactSerializer(serializers.ModelSerializer):
    street = serializers.CharField(max_length=255, required=False, allow_blank=True)
    ZIP_code = serializers.IntegerField(required=False, allow_null=True)
    city = serializers.CharField(max_length=255, required=False, allow_blank=True)
    country = serializers.ChoiceField(choices=COUNTRIES_CHOICES, required=False)
    address_type = serializers.ChoiceField(choices=ADDRESS_TYPE_CHOICES, required=False)

    class Meta:
        model = AddressForContact
        fields = '__all__'

    def validate_ZIP_code(self, value):
        if value is not None:
            zip_code_str = str(value)
            if not (len(zip_code_str) == 5 or len(zip_code_str) == 6) or not zip_code_str.isdigit():
                raise serializers.ValidationError("ZIP code must be 5 to 6 digits.")
        return value
    
    def validate_country(self, value):
        if value not in [country[0] for country in COUNTRIES_CHOICES]:
            raise serializers.ValidationError("Invalid country")
        return value

    def validate_address_type(self, value):
        if value not in [choice[0] for choice in ADDRESS_TYPE_CHOICES]:
            raise serializers.ValidationError("Invalid address type.")
        return value


class ContactDetailsForContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetailsForContact
        fields = '__all__'

    def validate_phone_type(self, value):
        if value and value not in dict(ContactDetailsForContact.CONTACT_CHOICES):
            raise serializers.ValidationError("Invalid phone type.")
        return value

    def validate_email_type(self, value):
        if value and value not in dict(ContactDetailsForContact.CONTACT_CHOICES):
            raise serializers.ValidationError("Invalid email type.")
        return value

    def validate_web_url_type(self, value):
        if value and value not in dict(ContactDetailsForContact.CONTACT_CHOICES):
            raise serializers.ValidationError("Invalid web url type.")
        return value



class PaymentInformationForContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInformationForContacts
        fields = '__all__'

    def validate_routing_number(self, value):
        if value is not None and (value < 0 or value > 999999):
            raise serializers.ValidationError("Routing number must be a positive integer between 0 and 999999.")
        return value

    def validate_swift_code(self, value):
        if value is not None and (value < 0 or value > 999999):
            raise serializers.ValidationError("Swift code must be a positive integer between 0 and 999999.")
        return value

    def validate_sales_tax_id(self, value):
        if value is not None and (value < 0 or value > 999999):
            raise serializers.ValidationError("Sales tax ID must be a positive integer between 0 and 999999.")
        return value

    def validate_tax_reference(self, value):
        if value is not None and not (len(value) >= 0 and len(value) <= 255):
            raise serializers.ValidationError("Tax reference must be between 0 and 255 characters.")
        return value



class ConditionsForContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionsForContacts
        fields = '__all__'

    def validate_cash_discount_days(self, value):
        if value is not None and (value < 0 or value > 365):
            raise serializers.ValidationError("Cash discount days must be between 0 and 365.")
        return value

    def validate_cash_discount_percent(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Cash discount percent must be between 0 and 100.")
        return value

    def validate_payment_due_days(self, value):
        if value is not None and (value < 0 or value > 365):
            raise serializers.ValidationError("Payment due days must be between 0 and 365.")
        return value

    def validate_customer_discount_type(self, value):
        if value is not None and value not in [choice[0] for choice in ConditionsForContacts.CUSTOMER_DISCOUNT_CHOICES]:
            raise serializers.ValidationError("Invalid customer discount type.")
        return value

    def validate_customer_discount_value(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Customer discount value cannot be negative.")
        return value

class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = '__all__'





















