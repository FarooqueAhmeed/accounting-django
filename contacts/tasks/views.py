from contacts.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.parsers import JSONParser
from .serializers import TaskSerializer
from rest_framework import status


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def manage_tasks(request):
    # Route to the appropriate function based on the HTTP method
    if request.method == 'GET':
        return get_tasks(request)
    elif request.method == 'POST':
        return post_task(request)
    elif request.method == 'PUT':
        return put_task(request)
    elif request.method == 'DELETE':
        return delete_task(request)
    else:
        return Response({'message': 'HTTP method not allowed'}, status=405)



def get_tasks(request):
    # Parse the incoming data to check for an 'id' parameter
    task_id = request.data.get('id')
    
    if task_id:
        # If an ID is provided, try to get the specific task
        try:
            task = Task.objects.get(pk=task_id, MyInfo=request.user)  # Assuming MyInfo is related to User
            serializer = TaskSerializer(task)
            return Response({'message': 'Task retrieved successfully.', 'tasks_data': serializer.data})
        except Task.DoesNotExist:
            return Response({'message': 'The task does not exist or you do not have permission to view it.'}, status=404)
    else:
        # If no ID is provided, get all tasks for the logged-in user
        tasks = Task.objects.filter(MyInfo=request.user)  # Adjust the filter according to your model relationship
        serializer = TaskSerializer(tasks, many=True)
        return Response({'message': 'Tasks retrieved successfully.', 'tasks_data': serializer.data})




def post_task(request):
    # Parse the incoming data and create a new task for the logged-in user
    data = request.data.copy()
    organization_id = data.get('organization')
    contact_id = data.get('contact')

    # At least one of organization or contact must be provided
    if organization_id is None and contact_id is None:
        return Response(
            {'message': 'An organization or contact must be provided.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    data['MyInfo'] = request.user.pk # Set the myinfo to the logged-in user's MyInfo
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


def put_task(request):
    # Parse the incoming data and update the task for the logged-in user
    data = request.data.copy()
    try:
        # Ensure the task belongs to the logged-in user
        task = Task.objects.get(pk=data.get('id'), myinfo=request.user.myinfo)
    except Task.DoesNotExist:
        return Response({'message': 'The task does not exist'}, status=404)
    
    serializer = TaskSerializer(task, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


def delete_task(request):
    # Parse the incoming data and delete the task for the logged-in user
    data = JSONParser().parse(request)
    try:
        # Ensure the task belongs to the logged-in user
        task = Task.objects.get(pk=data.get('id'), myinfo=request.user.myinfo)
        task.delete()
        return Response({'message': 'Task was deleted successfully!'}, status=204)
    except Task.DoesNotExist:
        return Response({'message': 'The task does not exist'}, status=404)
