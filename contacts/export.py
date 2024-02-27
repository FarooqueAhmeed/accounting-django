import datetime
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import A4,A3
from django.conf import settings
from my_company.models import *
User = get_user_model()
from contacts.models import *
from reportlab.lib.units import inch  
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import csv




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def export_organizations(request):
    export_format = request.data.get('format', None)

    if export_format not in ('csv', 'pdf'):
        return Response({'error': 'Invalid format. Use CSV or PDF.'}, status=400)

    if export_format == 'csv':
        # Export as CSV
        queryset = Organization.objects.filter(MyInfo=request.user)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="organizations.csv"'

        writer = csv.writer(response)
        writer.writerow(["Customer Number", "Name", "Street", "ZIP Code", "City", "Phone", "Email"])

        for org in queryset:
            latest_address = AddressForContact.objects.filter(organization=org).latest('id') if AddressForContact.objects.filter(organization=org).exists() else None
            latest_contact_details = ContactDetailsForContact.objects.filter(organization=org).latest('id') if ContactDetailsForContact.objects.filter(organization=org).exists() else None

            row = [
                org.customer_number,
                org.organization_name,
                latest_address.street if latest_address else "",
                latest_address.ZIP_code if latest_address else "",
                latest_address.city if latest_address else "",
                latest_contact_details.phone if latest_contact_details else "",
                latest_contact_details.email if latest_contact_details else "",
            ]

            writer.writerow(row)

        return response
    elif export_format == 'pdf':
        user = User.objects.get(email=request.user.email)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        user_email = user.email

        my_company_address = MyCompanyAddress.objects.filter(owner=user).first()
        if my_company_address:
            address = my_company_address.address
            zip_code = my_company_address.zip_code
            city = my_company_address.city
        else:
            address = ""
            zip_code = ""
            city = ""

        # Create a buffer to store the PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A3)

        # Create a list to hold the elements for the PDF
        elements = []

        # Title
        title = "All Organizations"
        styles = getSampleStyleSheet()
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 12))

        # User Information
        user_info = f'Email: {user_email}'
        elements.append(Paragraph(user_info, styles['Normal']))
        date_info = f'Date: {current_date}'
        elements.append(Paragraph(date_info, styles['Normal']))
        address_info = f'Address: {address}'
        elements.append(Paragraph(address_info, styles['Normal']))
        zip_code_info = f'Zip Code: {zip_code}'
        elements.append(Paragraph(zip_code_info, styles['Normal']))
        city_info = f'City: {city}'
        elements.append(Paragraph(city_info, styles['Normal']))

        elements.append(Spacer(1, 12))
        
        #filter organizations
        # Get all organizations associated with AddressForContact objects
        organizations = Organization.objects.filter(MyInfo=user)

        # Define the table header
        table_header = ["Customer Number", "Name", "Street", "ZIP Code", "City", "Phone", "Email"]

        data = []

        for org in organizations:
            # Get the latest address for the organization
            latest_address = AddressForContact.objects.filter(organization=org).latest('id') if AddressForContact.objects.filter(organization=org).exists() else None

            # Get the latest contact details for the organization
            latest_contact_details = ContactDetailsForContact.objects.filter(organization=org).latest('id') if ContactDetailsForContact.objects.filter(organization=org).exists() else None

            org_row = [
                org.customer_number,
                org.organization_name,
                latest_address.street if latest_address else "",  # Use the street from the latest address
                latest_address.ZIP_code if latest_address else "",
                latest_address.city if latest_address else "",
                latest_contact_details.phone if latest_contact_details else "",
                latest_contact_details.email if latest_contact_details else "",
            ]
            data.append(org_row)


        # Create the PDF table for organizations
        colWidths = [1.3 * inch, 2 * inch, 1.5 * inch, 1 * inch, 1 * inch, 2 * inch, 2 * inch]

        table = Table([table_header] + data, colWidths=colWidths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Add elements to the PDF
        elements.append(table)

        # Build the PDF document
        doc.build(elements)

        # Get the value of the buffer and return the response
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Organizations.pdf"'
        response.write(pdf)
        return response






@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def export_contacts(request):
    export_format = request.data.get('format', None)

    if export_format not in ('csv', 'pdf'):
        return Response({'error': 'Invalid format. Use CSV or PDF.'}, status=400)

    if export_format == 'csv':
        # Export as CSV
        queryset = Contact.objects.filter(MyInfo=request.user)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="contacts.csv"'

        writer = csv.writer(response)
        writer.writerow(["Customer Number", "Name", "Street", "ZIP Code", "City", "Phone", "Email"])

        for cnt in queryset:
            latest_address = AddressForContact.objects.filter(contact=cnt).latest('id') if AddressForContact.objects.filter(contact=cnt).exists() else None
            latest_contact_details = ContactDetailsForContact.objects.filter(contact=cnt).latest('id') if ContactDetailsForContact.objects.filter(contact=cnt).exists() else None

            row = [
                cnt.customer_number,
                cnt.first_name,
                latest_address.street if latest_address else "",
                latest_address.ZIP_code if latest_address else "",
                latest_address.city if latest_address else "",
                latest_contact_details.phone if latest_contact_details else "",
                latest_contact_details.email if latest_contact_details else "",
            ]

            writer.writerow(row)

        return response
    elif export_format == 'pdf':
        user = User.objects.get(email=request.user.email)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        user_email = user.email

        my_company_address = MyCompanyAddress.objects.filter(owner=user).first()
        if my_company_address:
            address = my_company_address.address
            zip_code = my_company_address.zip_code
            city = my_company_address.city
        else:
            address = ""
            zip_code = ""
            city = ""

        # Create a buffer to store the PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A3)

        # Create a list to hold the elements for the PDF
        elements = []

        # Title
        title = "All Contacts"
        styles = getSampleStyleSheet()
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 12))

        # User Information
        user_info = f'Email: {user_email}'
        elements.append(Paragraph(user_info, styles['Normal']))
        date_info = f'Date: {current_date}'
        elements.append(Paragraph(date_info, styles['Normal']))
        address_info = f'Address: {address}'
        elements.append(Paragraph(address_info, styles['Normal']))
        zip_code_info = f'Zip Code: {zip_code}'
        elements.append(Paragraph(zip_code_info, styles['Normal']))
        city_info = f'City: {city}'
        elements.append(Paragraph(city_info, styles['Normal']))

        elements.append(Spacer(1, 12))
        
        #filter Contact
        # Get all Contact 
        contacts = Contact.objects.filter(MyInfo=user)

        # Define the table header
        table_header = ["Customer Number", "Name", "Street", "ZIP Code", "City", "Phone", "Email"]

        data = []

        for cnt in contacts:
            # Get the latest address for the contacts
            latest_address = AddressForContact.objects.filter(contact=cnt).latest('id') if AddressForContact.objects.filter(contact=cnt).exists() else None

            # Get the latest contact details for the contacts
            latest_contact_details = ContactDetailsForContact.objects.filter(contact=cnt).latest('id') if ContactDetailsForContact.objects.filter(contact=cnt).exists() else None

            org_row = [
                cnt.customer_number,
                cnt.first_name,
                latest_address.street if latest_address else "",  # Use the street from the latest address
                latest_address.ZIP_code if latest_address else "",
                latest_address.city if latest_address else "",
                latest_contact_details.phone if latest_contact_details else "",
                latest_contact_details.email if latest_contact_details else "",
            ]
            data.append(org_row)


        # Create the PDF table for organizations
        colWidths = [1.3 * inch, 1.5 * inch, 2 * inch, 1 * inch, 1 * inch, 1.2 * inch, 2 * inch]

        table = Table([table_header] + data, colWidths=colWidths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Add elements to the PDF
        elements.append(table)

        # Build the PDF document
        doc.build(elements)

        # Get the value of the buffer and return the response
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="contacts.pdf"'
        response.write(pdf)
        return response