from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.conf import settings
from my_company.models import *
User = get_user_model()
from contacts.models import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv
from rest_framework.response import Response
from rest_framework.decorators import api_view
import io
import tabula
import pandas as pd






@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_organizations_from_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        # Check if the uploaded file is a CSV file based on its content type
        if not csv_file.content_type.startswith('text/csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)

        try:
            # Validate and get the user with the given email
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            return Response({'error': 'User not found with the provided request.'}, status=400)


        failed_count = 0
        success_count = 0
        skipped_count = 0

        try:
            with io.TextIOWrapper(csv_file, encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                # Check if the header row is as expected
                header = next(reader)
                expected_header = ['Customer Number', 'Name', 'Street', 'ZIP Code', 'City', 'Phone', 'Email']
                if header != expected_header:
                    # Find the incorrect column name
                    incorrect_columns = [col for col in header if col not in expected_header]
                    missing_columns = [col for col in expected_header if col not in header]
                    
                    if incorrect_columns:
                        return Response({'error': f'Invalid CSV header. The following column(s) are incorrect: {", ".join(incorrect_columns)}. Expected column names: {", ".join(expected_header)}'}, status=400)
                    if missing_columns:
                        return Response({'error': f'Invalid CSV header. The following column(s) are missing: {", ".join(missing_columns)}. Expected column names: {", ".join(expected_header)}'}, status=400)
                    
                    # Handle the case where extra columns are present
                    if len(header) > len(expected_header):
                        return Response({'error': 'Invalid CSV header. It contains extra columns.'}, status=400)


                organizations = []  # Collect organizations to be inserted in bulk
                addresses = []  # Collect addresses to be inserted in bulk
                contact_details = []  # Collect contact details to be inserted in bulk

                # Check if a Category object exists for the user
                user_category = Category.objects.filter(my_info=user).order_by('-created').first()

                # Create a default Category if none exists
                if not user_category:
                    user_category = Category.objects.create(
                        name="Default import Contact type",
                        category_type="contact",  # You can set the category type as needed
                        color="",  # You can set the color as needed
                        abbreviation="Default",
                        sale_or_purchase="sale",  # You can set the sale/purchase type as needed
                        overall_debtor_account="",
                        my_info=user,
                    )

                for row in reader:
                    # Ensure the row has the expected number of columns
                    if len(row) == 7:
                        print(f"CSV Row Data: {row}")  # Print the CSV row data

                        # Extract the row data
                        customer_number, organization_name, street, zip_code, city, phone, email = row

                        # Skip creating objects if organization_name and customer_number are empty
                        if not organization_name or not customer_number:
                            print("Skipped due to missing organization_name or customer_number")
                            skipped_count += 1
                            continue

                        # Auto-generate the name_suffix from organization_name
                        name_suffix = organization_name[:10]  # You can adjust the length as needed

                        # Validate ZIP code and convert it to an integer (if not empty)
                        if zip_code:
                            try:
                                zip_code = int(zip_code)
                            except ValueError:
                                return Response({'error': f'Invalid ZIP code: {zip_code}'}, status=400)

                        # Create the Organization object and add it to the list
                        organization = Organization(
                            organization_name=organization_name,
                            name_suffix=name_suffix,
                            customer_number=customer_number,
                            debtor_number=0,  # You can set the debtor_number as needed
                            MyInfo=user,
                            contact_type=user_category,
                        )
                        organizations.append(organization)

                        # Create the AddressForContact object and add it to the list
                        if zip_code:
                            address = AddressForContact(
                                street=street,
                                ZIP_code=zip_code,
                                city=city,
                                country='',  # You can set the country as needed
                                address_type='work',  # Set the address type as needed
                                organization=organization
                            )
                            addresses.append(address)

                        # Create the ContactDetailsForContact object and add it to the list
                        contact_detail = ContactDetailsForContact(
                            phone=phone,
                            email=email,
                            phone_type='work',  # Set the phone type as needed
                            email_type='work',  # Set the email type as needed
                            web_url='',  # You can set the web_url as needed
                            organization=organization
                        )
                        contact_details.append(contact_detail)
                    
                # Bulk insert organizations, addresses, and contact details
                Organization.objects.bulk_create(organizations)
                AddressForContact.objects.bulk_create(addresses)
                ContactDetailsForContact.objects.bulk_create(contact_details)

                success_count = len(organizations)

            return Response({
                'message': 'Data imported successfully',
                'success_count': success_count,
                'failed_count': failed_count,
                'skipped_count': skipped_count,
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)

    return Response({'error': 'Invalid request'}, status=400)








@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_contacts_from_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        # Check if the uploaded file is a CSV file based on its content type
        if not csv_file.content_type.startswith('text/csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)

        try:
            # Validate and get the user with the given email
            user = User.objects.filter(email=request.user.email).first()
            if not user:
                return Response({'error': 'User not found with the provided email.'}, status=400)

            failed_count = 0
            success_count = 0
            skipped_count = 0

            with io.TextIOWrapper(csv_file, encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                # Check if the header row is as expected
                header = next(reader)
                expected_header = ['Customer Number', 'Name', 'Street', 'ZIP Code', 'City', 'Phone', 'Email']
                if header != expected_header:
                    # Find the incorrect column name
                    incorrect_columns = [col for col in header if col not in expected_header]
                    missing_columns = [col for col in expected_header if col not in header]
                    
                    if incorrect_columns:
                        return Response({'error': f'Invalid CSV header. The following column(s) are incorrect: {", ".join(incorrect_columns)}. Expected column names: {", ".join(expected_header)}'}, status=400)
                    if missing_columns:
                        return Response({'error': f'Invalid CSV header. The following column(s) are missing: {", ".join(missing_columns)}. Expected column names: {", ".join(expected_header)}'}, status=400)
                    
                    # Handle the case where extra columns are present
                    if len(header) > len(expected_header):
                        return Response({'error': 'Invalid CSV header. It contains extra columns.'}, status=400)
                

                contacts = []  # Collect contacts to be inserted in bulk
                addresses = []  # Collect addresses to be inserted in bulk
                contact_details = []  # Collect contact details to be inserted in bulk

                # Check if a Category object exists for the user
                user_category = Category.objects.filter(my_info=user).order_by('-created').first()

                # Create a default Category if none exists
                if not user_category:
                    user_category = Category.objects.create(
                        name="Default import Contact type",
                        category_type="contact",  # You can set the category type as needed
                        color="",  # You can set the color as needed
                        abbreviation="Default",
                        sale_or_purchase="sale",  # You can set the sale/purchase type as needed
                        overall_debtor_account="",
                        my_info=user,
                    )

                for row in reader:
                    # Ensure the row has the expected number of columns
                    if len(row) == 7:
                        print(f"CSV Row Data: {row}")  # Print the CSV row data

                        # Extract the row data
                        customer_number, first_name, street, zip_code, city, phone, email = row

                        # Skip creating objects if first_name and customer_number are empty
                        if not first_name or not customer_number:
                            print("Skipped due to missing first_name or customer_number")
                            skipped_count += 1
                            continue

                        # Auto-generate the name_suffix from first_name
                        name_suffix = first_name[:10]  # You can adjust the length as needed

                        # Validate ZIP code and convert it to an integer (if not empty)
                        if zip_code:
                            try:
                                zip_code = int(zip_code)
                            except ValueError:
                                return Response({'error': f'Invalid ZIP code: {zip_code}'}, status=400)

                        # Create the Contact object and add it to the list
                        contact = Contact(
                            salutation="Mr",  # You can set the salutation as needed
                            title="",  # You can set the title as needed
                            first_name=first_name,
                            last_name="",  # You can set the last_name as needed
                            legal_name="",  # You can set the legal_name as needed
                            customer_number=customer_number,
                            line_item="",  # You can set the line_item as needed
                            debtor_number=0,  # You can set the debtor_number as needed
                            MyInfo=user,
                            contact_type=user_category,  # Assign the contact_type based on your requirements
                        )
                        contacts.append(contact)

                        # Create the AddressForContact object and add it to the list
                        if zip_code:
                            address = AddressForContact(
                                street=street,
                                ZIP_code=zip_code,
                                city=city,
                                country='',  # You can set the country as needed
                                address_type='work',  # Set the address type as needed
                                contact=contact
                            )
                            addresses.append(address)

                        # Create the ContactDetailsForContact object and add it to the list
                        contact_detail = ContactDetailsForContact(
                            phone=phone,
                            email=email,
                            phone_type='work',  # Set the phone type as needed
                            email_type='work',  # Set the email type as needed
                            web_url='',  # You can set the web_url as needed
                            contact=contact
                        )
                        contact_details.append(contact_detail)

                # Bulk insert contact, addresses, and contact details
                Contact.objects.bulk_create(contacts)
                AddressForContact.objects.bulk_create(addresses)
                ContactDetailsForContact.objects.bulk_create(contact_details)

                success_count = len(contacts)

            return Response({
                'message': 'Data imported successfully',
                'success_count': success_count,
                'failed_count': failed_count,
                'skipped_count': skipped_count,
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)

    return Response({'error': 'Invalid request'}, status=400)





@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_org_data_from_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']

        # File format validation: Check if the uploaded file is a PDF
        if not pdf_file.name.endswith('.pdf'):
            return Response({'error': 'Invalid file format. Please upload a PDF file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use Tabula to extract tables from the PDF file
            tables = tabula.read_pdf(pdf_file)

            if not tables:
                return Response({'error': 'No tables found in the PDF'}, status=status.HTTP_400_BAD_REQUEST)

            # Assuming there is only one table on the page
            table = tables[0]

            # Expected column names
            expected_columns = ["Customer Number", "Name", "Street", "ZIP Code", "City", "Phone", "Email"]

            # Check if all expected columns are present
            missing_columns = [column for column in expected_columns if column not in table.columns]
            incorrect_columns = [column for column in table.columns if column not in expected_columns]

            if missing_columns or incorrect_columns:
                error_message = "Error in PDF table columns:\n"

                if missing_columns:
                    error_message += f"Missing columns: {', '.join(missing_columns)}\n"

                if incorrect_columns:
                    error_message += f"Incorrect columns: {', '.join(incorrect_columns)}\n"

                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            # Rename columns to match your data
            table.columns = expected_columns

            # Convert the table data to a list of dictionaries
            data = table.to_dict(orient="records")

            organizations = []  # Collect organizations to be inserted in bulk
            addresses = []  # Collect addresses to be inserted in bulk
            contact_details = []  # Collect contact details to be inserted in bulk

            failed_count = 0
            success_count = 0
            skipped_count = 0

            # Check if a Category object exists for the user
            user_category = Category.objects.filter(my_info=request.user).order_by('-created').first()

            # Create a default Category if none exists
            if not user_category:
                user_category = Category.objects.create(
                    name="Default import Contact type",
                    category_type="contact",  # You can set the category type as needed
                    color="",  # You can set the color as needed
                    abbreviation="Default",
                    sale_or_purchase="sale",  # You can set the sale/purchase type as needed
                    overall_debtor_account="",
                    my_info=request.user,
                )

            for row in data:
                customer_number = row["Customer Number"]
                name = row["Name"]
                street = row["Street"]
                zip_code = row["ZIP Code"]
                city = row["City"]
                phone = row["Phone"]
                email = row["Email"]

                if not name or not customer_number:
                    # Skip creating objects if organization_name and customer_number are empty
                    skipped_count += 1
                    continue

                # Auto-generate the name_suffix from the organization_name
                name_suffix = name[:10]  # You can adjust the length as needed

                # Validate ZIP code and convert it to an integer (if not empty)
                if zip_code:
                    try:
                        zip_code = int(zip_code)
                    except ValueError:
                        failed_count += 1
                        continue

                # Create the Organization object and add it to the list
                organization = Organization(
                    organization_name=name,
                    name_suffix=name_suffix,
                    customer_number=customer_number,
                    debtor_number=0,  # You can set the debtor_number as needed
                    MyInfo=request.user,
                    contact_type=user_category,
                )
                organizations.append(organization)

                # Create the AddressForContact object and add it to the list
                if zip_code:
                    address = AddressForContact(
                        street=street,
                        ZIP_code=zip_code,
                        city=city,
                        country='',  # You can set the country as needed
                        address_type='work',  # Set the address type as needed
                        organization=organization
                    )
                    addresses.append(address)

                # Create the ContactDetailsForContact object and add it to the list
                contact_detail = ContactDetailsForContact(
                    phone=phone,
                    email=email,
                    phone_type='work',  # Set the phone type as needed
                    email_type='work',  # Set the email type as needed
                    web_url='',  # You can set the web_url as needed
                    organization=organization
                )
                contact_details.append(contact_detail)
                success_count += 1

            # Bulk insert organizations, addresses, and contact details
            Organization.objects.bulk_create(organizations)
            AddressForContact.objects.bulk_create(addresses)
            ContactDetailsForContact.objects.bulk_create(contact_details)

            return Response({
                'message': 'Data imported successfully',
                'success_count': success_count,
                'failed_count': failed_count,
                'skipped_count': skipped_count,
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)








@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_contacts_data_from_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']

        # File format validation: Check if the uploaded file is a PDF
        if not pdf_file.name.endswith('.pdf'):
            return Response({'error': 'Invalid file format. Please upload a PDF file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use Tabula to extract tables from the PDF file
            tables = tabula.read_pdf(pdf_file)

            if not tables:
                return Response({'error': 'No tables found in the PDF'}, status=status.HTTP_400_BAD_REQUEST)

            # Assuming there is only one table on the page
            table = tables[0]

            # Expected column names
            expected_columns = ["Customer Number", "Name", "Street", "ZIP Code", "City", "Phone", "Email"]

            # Check if all expected columns are present
            missing_columns = [column for column in expected_columns if column not in table.columns]
            incorrect_columns = [column for column in table.columns if column not in expected_columns]

            if missing_columns or incorrect_columns:
                error_message = "Error in PDF table columns:\n"

                if missing_columns:
                    error_message += f"Missing columns: {', '.join(missing_columns)}\n"

                if incorrect_columns:
                    error_message += f"Incorrect columns: {', '.join(incorrect_columns)}\n"

                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            # Rename columns to match your data
            table.columns = expected_columns

            # Convert the table data to a list of dictionaries
            data = table.to_dict(orient="records")

            contacts = []  # Collect contacts to be inserted in bulk
            addresses = []  # Collect addresses to be inserted in bulk
            contact_details = []  # Collect contact details to be inserted in bulk

            failed_count = 0
            success_count = 0
            skipped_count = 0

            # Check if a Category object exists for the user
            user_category = Category.objects.filter(my_info=request.user).order_by('-created').first()

            # Create a default Category if none exists
            if not user_category:
                user_category = Category.objects.create(
                    name="Default import Contact type",
                    category_type="contact",  # You can set the category type as needed
                    color="",  # You can set the color as needed
                    abbreviation="Default",
                    sale_or_purchase="sale",  # You can set the sale/purchase type as needed
                    overall_debtor_account="",
                    my_info=request.user,
                )

            for row in data:
                customer_number = row["Customer Number"]
                name = row["Name"]
                street = row["Street"]
                zip_code = row["ZIP Code"]
                city = row["City"]
                phone = row["Phone"]
                email = row["Email"]

                if not name or not customer_number:
                    # Skip creating objects if organization_name and customer_number are empty
                    skipped_count += 1
                    continue

                # Validate ZIP code and convert it to an integer (if not empty)
                if zip_code:
                    try:
                        zip_code = int(zip_code)
                    except ValueError:
                        failed_count += 1
                        continue

                # Create the Contact object and add it to the list
                contact = Contact(
                            salutation="Mr",  # You can set the salutation as needed
                            title="",  # You can set the title as needed
                            first_name=name,
                            last_name="",  # You can set the last_name as needed
                            legal_name="",  # You can set the legal_name as needed
                            customer_number=customer_number,
                            line_item="",  # You can set the line_item as needed
                            debtor_number=0,  # You can set the debtor_number as needed
                            MyInfo=request.user,
                            contact_type=user_category,  # Assign the contact_type based on your requirements
                )
                contacts.append(contact)

                # Create the AddressForContact object and add it to the list
                if zip_code:
                    address = AddressForContact(
                        street=street,
                        ZIP_code=zip_code,
                        city=city,
                        country='',  # You can set the country as needed
                        address_type='work',  # Set the address type as needed
                        contact=contact
                    )
                    addresses.append(address)

                # Create the ContactDetailsForContact object and add it to the list
                contact_detail = ContactDetailsForContact(
                    phone=phone,
                    email=email,
                    phone_type='work',  # Set the phone type as needed
                    email_type='work',  # Set the email type as needed
                    web_url='',  # You can set the web_url as needed
                    contact=contact
                )
                contact_details.append(contact_detail)
                success_count += 1

            # Bulk insert contact, addresses, and contact details
            Contact.objects.bulk_create(contacts)
            AddressForContact.objects.bulk_create(addresses)
            ContactDetailsForContact.objects.bulk_create(contact_details)

            return Response({
                'message': 'Data imported successfully',
                'success_count': success_count,
                'failed_count': failed_count,
                'skipped_count': skipped_count,
            })

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)