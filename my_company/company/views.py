from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.http import Http404
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from my_company.models import *
from my_company.company.serializers import *
from my_company.my_info.serializers import *



@api_view(['GET', 'PUT', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_company_address(request):
    if request.method == 'GET' or request.method == 'PUT':
        try:
            # Filter the MyCompanyAddress object for the authenticated user
            company_address = MyCompanyAddress.objects.get(owner=request.user)
        except MyCompanyAddress.DoesNotExist:
            return Response({'error': 'Company address not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return get_company_address(request, company_address)
    elif request.method == 'PUT':
        return update_company_address(request, company_address)
    elif request.method == 'POST':
        return create_company_address(request)





def get_company_address(request, company_address):
    # Assuming there's a foreign key relationship with MyInfo model, access the associated MyInfo user data
    user_data = {
        'company_address': MyCompanyAddressSerializer(company_address).data,
        'user_info': MyInfoSerializer(company_address.owner).data,
        'message':f"Successfully fetched your company {company_address.legal_company_name}"
    }
    return Response(user_data)

def update_company_address(request, company_address):
    # Check if the user is attempting to update their own data
    if company_address.owner != request.user:
        return Response({'error': 'You do not have permission to update this company address.'}, status=status.HTTP_403_FORBIDDEN)

    # Update the MyCompanyAddress object with the request data
    serializer = MyCompanyAddressSerializer(company_address, data=request.data, partial=True)
    if serializer.is_valid():
        # Set the owner field to the current user
        serializer.validated_data['owner'] = request.user
        serializer.save()
        response_data = {
            "message": f"Updated successfully: {serializer.validated_data['legal_company_name']}",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_company_address(request):
    # Check if a MyCompanyAddress instance already exists for the user
    existing_instance = MyCompanyAddress.objects.filter(owner=request.user).first()
    if existing_instance:
        return Response({'error': 'A Company Address instance already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MyCompanyAddressSerializer(data=request.data)
    if serializer.is_valid():
        # Set the owner to the authenticated user
        serializer.validated_data['owner'] = request.user
        serializer.save()

        response_data = {
            "message": f"Successfully created, {serializer.validated_data['legal_company_name']}",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_company_tax_info(request):
    # Check the HTTP method and call the corresponding function
    if request.method == 'GET':
        return get_my_company_tax_info(request)
    elif request.method == 'PUT':
        return update_my_company_tax_info(request)
    elif request.method == 'POST':
        return create_my_company_tax_info(request)


def create_my_company_tax_info(request):
    # Check if a MyCompanyTaxInfo instance already exists for the user
    existing_instance = MyCompanyTaxInfo.objects.filter(my_company_address__owner=request.user).first()
    if existing_instance:
        return Response({'error': 'A Company Tax Info instance already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the related MyCompanyAddress for the requested user
    try:
        my_company_address = MyCompanyAddress.objects.get(owner=request.user)
    except MyCompanyAddress.DoesNotExist:
        return Response({'error': 'Related Company Address not found'}, status=status.HTTP_404_NOT_FOUND)

    # Add the MyCompanyAddress to the request data
    request.data['my_company_address'] = my_company_address.pk

    # Serialize and save the MyCompanyTaxInfo instance
    serializer = MyCompanyTaxInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "message": "Your Company Tax Info has been added",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_my_company_tax_info(request):
    try:
        # Retrieve the MyCompanyTaxInfo instance for the authenticated user
        tax_info = MyCompanyTaxInfo.objects.get(my_company_address__owner=request.user)
        tax_info_serializer = MyCompanyTaxInfoSerializer(tax_info)
        
        # Retrieve related user data
        user_data = MyInfoSerializer(tax_info.my_company_address.owner).data

        # Retrieve related company address data using MyCompanyAddressSerializer
        company_address_data = MyCompanyAddressSerializer(tax_info.my_company_address).data

        # Combine tax info, company address data, and user data in the response
        response_data = {
            "message": "Your company Tax Info has been fetched",
            'company_tax_info': tax_info_serializer.data,
            'company_address_data': company_address_data,
            'user_info': user_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except MyCompanyTaxInfo.DoesNotExist:
        return Response({'error': 'Company Tax Info not found'}, status=status.HTTP_404_NOT_FOUND)

def update_my_company_tax_info(request):
    try:
        # Retrieve the MyCompanyTaxInfo instance for the authenticated user
        tax_info = MyCompanyTaxInfo.objects.get(my_company_address__owner=request.user)
    except MyCompanyTaxInfo.DoesNotExist:
        return Response({'error': 'Company Tax Info not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Check if the authenticated user is updating their own object
        if tax_info.my_company_address.owner != request.user:
            raise ValidationError("You do not have permission to update this object.")
        
        serializer = MyCompanyTaxInfoSerializer(tax_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Your Company Tax Info has been updated",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_tags(request):
    if request.method == 'GET':
        id = request.data.get('id')
        if id is not None:
            # Check if the requested tag belongs to the authenticated user
            try:
                tag = Tags.objects.get(pk=id, my_info=request.user)
                return get_tag_detail(request)
            except Tags.DoesNotExist:
                return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return get_tags(request)
    elif request.method == 'POST':
        return create_tag(request)
    elif request.method == 'PUT':
        id = request.data.get('id')
        if id is not None:
            # Check if the user is updating their own tag
            try:
                tag = Tags.objects.get(pk=id, my_info=request.user)
                return update_tag_detail(request)
            except Tags.DoesNotExist:
                return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Tag ID is required for updating'}, status=status.HTTP_400_BAD_REQUEST)




def create_tag(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    # Add request.user to the my_info field
    request.data['my_info'] = request.user.pk
    
    serializer = TagsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "message": "Tag has been created successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_tags(request):
    # Retrieve all Tags instances related to the authenticated user
    tags = Tags.objects.filter(my_info=request.user)
    serializer = TagsSerializer(tags, many=True)
    response_data = {
        "message": "Tags retrieved successfully",
        "data": serializer.data,
        "user_info": {
            "user_id": request.user.id,
            "user_email": request.user.email,
            "user_name": f"{request.user.first_name} {request.user.last_name}",
        },
    }
    return Response(response_data, status=status.HTTP_200_OK)




def get_tag_detail(request):
    # Retrieve the 'id' from the JSON data in the request
    pk = request.data.get('id')

    try:
        tag = Tags.objects.get(pk=pk)
    except Tags.DoesNotExist:
        return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the tag belongs to the authenticated user
    if tag.my_info != request.user:
        return Response({'error': 'You do not have permission to access this tag.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = TagsSerializer(tag)
    response_data = {
        "message": "Tag details retrieved successfully",
        "data": serializer.data,
        "user_info": {
            "user_id": request.user.id,
            "user_email": request.user.email,
            "user_name": f"{request.user.first_name} {request.user.last_name}",
        },
    }
    return Response(response_data, status=status.HTTP_200_OK)



def update_tag_detail(request):
    pk = request.data.get('id')
    name = request.data.get('name')

    if pk is not None:
        try:
            tag = Tags.objects.get(pk=pk)
        except Tags.DoesNotExist:
            return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is trying to update their own tag
        if tag.my_info != request.user:
            raise PermissionDenied("You do not have permission to update this tag.")

        serializer = TagsSerializer(tag, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(my_info=request.user, name=name)  # Update the my_info and name fields
            response_data = {
                "message": "Tag details updated successfully",
                "data": serializer.data,
                "user_info": {
                    "user_id": request.user.id,
                    "user_email": request.user.email,
                    "user_name": f"{request.user.first_name} {request.user.last_name}",
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Tag "id" not provided in the JSON data'}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET', 'PUT', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_company_contact_info(request):

    if request.method == 'GET':
        return get_my_company_contact_info(request)
    elif request.method == 'PUT':
        return update_my_company_contact_info(request)
    elif request.method == 'POST':
        return create_my_company_contact_info(request)
    



def get_my_company_contact_info(request):
    try:
        # Retrieve the MyCompanyContactInfo instance for the authenticated user
        contact_info = MyCompanyContactInfo.objects.get(my_company_address__owner=request.user)
        contact_info_serializer = MyCompanyContactInfoSerializer(contact_info)
        
        # Retrieve related user data
        user_data = MyInfoSerializer(contact_info.my_company_address.owner).data

        # Retrieve related company address data
        company_address_data = MyCompanyAddressSerializer(contact_info.my_company_address).data

        # Combine contact info, user data, and company address data in the response
        response_data = {
            'message': "Your Company Contact Info has been fetched",
            'company_contact_info': contact_info_serializer.data,
            'user_info': user_data,
            'company_address_data': company_address_data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except MyCompanyContactInfo.DoesNotExist:
        return Response({'error': 'Company Contact Info not found'}, status=status.HTTP_404_NOT_FOUND)



def update_my_company_contact_info(request):
    # Check if the authenticated user owns the contact_info
    try:
        contact_info = MyCompanyContactInfo.objects.get(my_company_address__owner=request.user)
    except MyCompanyContactInfo.DoesNotExist:
        return Response({'error': 'Contact Info not found for the authenticated user.'}, status=status.HTTP_404_NOT_FOUND)

    if contact_info.my_company_address.owner == request.user:
        # Check if the tags are related to and created by the request.user
        tag_ids = request.data.get('tags', [])
        for tag_id in tag_ids:
            try:
                tag = Tags.objects.get(id=tag_id, my_info=request.user)
            except Tags.DoesNotExist:
                return Response({'error': 'One or more tags are invalid or do not belong to you.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MyCompanyContactInfoSerializer(contact_info, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Serialize the MyCompanyAddress and Contact Info instances
            my_company_address_serializer = MyCompanyAddressSerializer(contact_info.my_company_address)
            contact_info_serializer = serializer

            response_data = {
                "message": "Your Company Contact Info has been updated",
                "my_company_address": my_company_address_serializer.data,
                "contact_info_data": contact_info_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied("You do not have permission to update this contact info.")

def create_my_company_contact_info(request):
    # Check if a MyCompanyContactInfo instance already exists for the user
    existing_instance = MyCompanyContactInfo.objects.filter(my_company_address__owner=request.user).first()
    if existing_instance:
        return Response({'error': 'A Company Contact Info instance already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the related MyCompanyAddress for the requested user
    try:
        my_company_address = MyCompanyAddress.objects.get(owner=request.user)
    except MyCompanyAddress.DoesNotExist:
        return Response({'error': 'Related Company Address not found'}, status=status.HTTP_404_NOT_FOUND)

    # Add the MyCompanyAddress to the request data
    request.data['my_company_address'] = my_company_address.pk

    serializer = MyCompanyContactInfoSerializer(data=request.data)
    if serializer.is_valid():
        # Set the MyCompanyAddress for the new instance
        serializer.validated_data['my_company_address'] = my_company_address

        # Check if the tags are related to and created by the request.user
        tags_data = request.data.get('tags')
        if tags_data:
            for tag_id in tags_data:
                try:
                    tag = Tags.objects.get(pk=tag_id, my_info=request.user)
                except Tags.DoesNotExist:
                    return Response({'error': f'Tag with ID {tag_id} is not related to or created by {request.user.first_name}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        # Serialize the MyCompanyAddress and Contact Info instances
        my_company_address_serializer = MyCompanyAddressSerializer(my_company_address)
        contact_info_serializer = serializer

        response_data = {
            "message": "Your Company Contact Info has been added",
            "contact_info_data": contact_info_serializer.data,
            "my_company_address": my_company_address_serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_company_payment_info(request):
    if request.method == 'GET':
        return get_my_company_payment_info(request)
    elif request.method == 'POST':
        return create_my_company_payment_info(request)
    elif request.method == 'PUT':
        return update_my_company_payment_info(request)

def get_my_company_payment_info(request):
    try:
        # Retrieve the MyCompanyPaymentInfo instance for the authenticated user
        payment_info = MyCompanyPaymentInfo.objects.get(my_company_address__owner=request.user)
        payment_info_serializer = MyCompanyPaymentInfoSerializer(payment_info)

        # Retrieve related MyCompanyAddress data
        company_address_data = MyCompanyAddressSerializer(payment_info.my_company_address).data

        # Combine payment info and MyCompanyAddress data in the response
        response_data = {
            'message': 'Company payment info instance fetched successfully',
            'company_payment_info': payment_info_serializer.data,
            'company_address_data': company_address_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except MyCompanyPaymentInfo.DoesNotExist:
        return Response({'error': 'Company Payment Info not found'}, status=status.HTTP_404_NOT_FOUND)

def create_my_company_payment_info(request):
    # Check if a MyCompanyPaymentInfo instance already exists for the user
    existing_instance = MyCompanyPaymentInfo.objects.filter(my_company_address__owner=request.user).first()
    if existing_instance:
        return Response({'error': 'A Company Payment Info instance already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the related MyCompanyAddress for the requested user
    try:
        my_company_address = MyCompanyAddress.objects.get(owner=request.user)
    except MyCompanyAddress.DoesNotExist:
        return Response({'error': 'Related Company Address not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create the MyCompanyPaymentInfo instance with the related MyCompanyAddress
    data = request.data
    data['my_company_address'] = my_company_address.pk
    serializer = MyCompanyPaymentInfoSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return_data = {
            'message': 'Company payment info instance created successfully',
            'my_company_payment_info': serializer.data,
            'my_company_address': MyCompanyAddressSerializer(my_company_address).data  # Adjust serializer as needed
        }
        return Response(return_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_my_company_payment_info(request):
    try:
        # Retrieve the MyCompanyPaymentInfo instance for the authenticated user
        payment_info = MyCompanyPaymentInfo.objects.get(my_company_address__owner=request.user)
    except MyCompanyPaymentInfo.DoesNotExist:
        return Response({'error': 'Company Payment Info not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the authenticated user is updating their own data
    if payment_info.my_company_address.owner != request.user:
        return Response({'error': 'You are not authorized to update this data.'}, status=status.HTTP_403_FORBIDDEN)

    # Update the MyCompanyPaymentInfo instance with the request data
    serializer = MyCompanyPaymentInfoSerializer(payment_info, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Company payment info instance updated successfully', 'data': serializer.data, 'my_company_address': MyCompanyAddressSerializer(payment_info.my_company_address).data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_company_logo(request):
    if isinstance(request, HttpRequest):
        request = Request(request)  # Convert to DRF Request if it's not

    if request.method == 'GET':
        return get_company_logo(request)
    elif request.method == 'POST':
        return create_company_logo(request)
    elif request.method == 'PUT':
        return update_company_logo(request)
    elif request.method == 'DELETE':
        return delete_company_logo(request)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_company_logo(request):
    try:
        # Retrieve the MyCompanyLogo instance for the authenticated user's company address
        company_address = MyCompanyAddress.objects.get(owner=request.user)
        company_logo = MyCompanyLogo.objects.get(company_address=company_address)
        serializer = MyCompanyLogoSerializer(company_logo)
        # Retrieve MyCompanyAddress data as well
        company_address_data = MyCompanyAddressSerializer(company_address).data
        return Response({'message': 'Company logo instance fetched successfully','company_logo': serializer.data, 'company_address': company_address_data}, status=status.HTTP_200_OK)
    except (MyCompanyAddress.DoesNotExist, MyCompanyLogo.DoesNotExist):
        raise Http404("Company logo not found")

def create_company_logo(request):
    # Check if a MyCompanyLogo instance already exists for the user's company address
    try:
        company_address = MyCompanyAddress.objects.get(owner=request.user)
        existing_logo = MyCompanyLogo.objects.get(company_address=company_address)
        return Response({'error': 'A Company Logo instance already exists for this company address.'},
                        status=status.HTTP_400_BAD_REQUEST)
    except (MyCompanyAddress.DoesNotExist, MyCompanyLogo.DoesNotExist):
        # The logo does not exist, proceed with creating it
        serializer = MyCompanyLogoSerializer(data=request.data)
        if serializer.is_valid():
            logo = serializer.save(company_address=company_address)
            # Create a serializer for the company address
            company_address_serializer = MyCompanyAddressSerializer(company_address)
            return Response({'message': 'Company logo instance created successfully', 'logo': serializer.data, 'company_address': company_address_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_company_logo(request):
    try:
        # Retrieve the MyCompanyLogo instance for the authenticated user's company address
        company_address = MyCompanyAddress.objects.get(owner=request.user)
        company_logo = MyCompanyLogo.objects.get(company_address=company_address)

        # Check if the authenticated user is updating their own data
        if company_logo.company_address.owner != request.user:
            return Response({'error': 'You are not authorized to update this data.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = MyCompanyLogoSerializer(company_logo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Get the updated company address
            updated_company_address = MyCompanyAddress.objects.get(owner=request.user)
            return Response({'message': 'Logo updated successfully', 'logo': serializer.data, 'company_address': MyCompanyAddressSerializer(updated_company_address).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except (MyCompanyAddress.DoesNotExist, MyCompanyLogo.DoesNotExist):
        raise Http404("Company logo not found")


def delete_company_logo(request):
    try:
        # Retrieve the MyCompanyLogo instance for the authenticated user's company address
        company_logo = MyCompanyLogo.objects.get(company_address__owner=request.user)

        # Check if the authenticated user is deleting their own data
        if company_logo.company_address.owner != request.user:
            return Response({'error': 'You are not authorized to delete this data.'}, status=status.HTTP_403_FORBIDDEN)

        company_logo.delete()
        return Response({'message': 'Company Logo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except MyCompanyLogo.DoesNotExist:
        return Response({'error': 'Company Logo not found'}, status=status.HTTP_404_NOT_FOUND)







@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def category_api(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        category_id = request.data.get('category_id')
        
        # Retrieve the MyInfo object associated with the authenticated user
        my_info = MyInfo.objects.get(email=request.user.email)

        if category_id:
            # Retrieve a specific category if the 'category_id' is provided
            try:
                category = Category.objects.get(id=category_id, my_info=my_info)
                serializer = CategorySerializer(category)
                response_data = {
                    'message': 'Category fetched successfully',
                    'my_info': MyInfoSerializer(my_info).data,
                    'category': serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({'error': 'Category not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Return all categories related to the authenticated user
            categories = Category.objects.filter(my_info=my_info)
            serializer = CategorySerializer(categories, many=True)
            response_data = {
                'message': 'Categories fetched successfully',
                'my_info': MyInfoSerializer(my_info).data,
                'categories': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            # Get the MyInfo object for the authenticated user
            my_info = MyInfo.objects.get(email=request.user.email)  # Assuming email is the identifier

            # Assign the MyInfo object to the 'my_info' field in the request data
            request.data['my_info'] = my_info.pk  # Set the 'my_info' field to the primary key of MyInfo

            # Create a new Category object with the provided data
            serializer = CategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Category created successfully', 'my_info': MyInfoSerializer(my_info).data, 'category': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except MyInfo.DoesNotExist:
            return Response({'error': 'MyInfo not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'PUT':
        category_id = request.data.get('category_id')
        if not category_id:
            return Response({'error': 'Category ID is required for the PUT request.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the requested Category belongs to the authenticated user
        category = Category.objects.filter(id=category_id, my_info__email=request.user.email).first()
        if not category:
            return Response({'error': 'Category not found for the authenticated user.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the existing Category with the JSON data
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Retrieve the updated MyInfo data
            my_info = MyInfo.objects.get(email=request.user.email)
            response_data = {
                'message': 'Category updated successfully',
                'my_info': MyInfoSerializer(my_info).data,
                'category': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category_id = request.data.get('category_id')
        if not category_id:
            return Response({'error': 'Category ID is required for the DELETE request.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the requested Category belongs to the authenticated user
        category = Category.objects.filter(id=category_id, my_info__email=request.user.email).first()
        if not category:
            return Response({'error': 'Category not found for the authenticated user.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the Category
        category.delete()
        # Retrieve the updated MyInfo data
        my_info = MyInfo.objects.get(email=request.user.email)
        response_data = {
            'message': 'Category deleted successfully',
            'my_info': MyInfoSerializer(my_info).data
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)














