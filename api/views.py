from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from base.models import Task
from . serializers import TaskSerializer, UserSerializer
import jwt, datetime 

# Create your views here.
@api_view(['POST'])
def registerUser(request):
    serializer = UserSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def loginUser(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()
    if user is None:
        raise AuthenticationFailed(f"A user with username '{username}' does not exist!")
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect Password")

    payload = {
        "id":user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat":datetime.datetime.utcnow()
    }

    token = jwt.encode(payload,'secret',algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        "jwt":token
    }

    return response

@api_view(['GET'])
def userView(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("User not authenticated")

    try:
        payload = jwt.decode(token, 'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("User not authenticated")

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def logoutUser(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("User not authenticated!")
    response = Response()
    response.delete_cookie('jwt')
    response.data = {"success":{"message":"User successfully logged out!"}}
    return response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/tasks',
        'GET /api/tasks/:id',
        'POST /api/tasks-create',
        'POST /api/tasks-update/:id',
        'DELETE /api/tasks-delete/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getTasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTask(request, pk):
    task = Task.objects.filter(id=pk).first()
    if task:
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)  
    else:
        return Response({"error":f"The task with the id {pk} does not exist!"})

@api_view(['POST'])
def createTask(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def updateTask(request,pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance = task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteTask(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response("Task successfully deleted!")
