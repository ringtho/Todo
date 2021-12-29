from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from base.models import Task
from . serializers import TaskSerializer, UserSerializer, LogoutSerializer
from .permissions import IsOwner

# Create your views here.
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

    user = authenticate(username=username, password=password)
    refresh = RefreshToken.for_user(user)
    
    token = {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }
    response = Response()
    response.set_cookie(key='jwt', value=token['access'], httponly=True)
    response.data = {
        'jwt':token
    }
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwner])
def getUser(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Please login to access this route!")
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsOwner])
def logoutUser(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Please login to access this route!")

    
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token).blacklist()
        response = Response()
        response.delete_cookie('jwt')
        response.data = {"success": "User successfully logged out!"}
        return response
    except Exception as e:
        message = {"error":"Invalid or expired token!"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsOwner])
def tasksViews(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Please login to access this route!")

    if request.method == 'GET':
        user = request.user
        tasks = user.task_set.all()
        if not tasks:
            return Response({"error":f"You haven't created any tasks yet!"})
        else:
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
    else:
        user = request.user
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated, IsOwner])
def taskViews(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Please login to access this route!")
    user=request.user
    task = user.task_set.filter(id=pk).first()
    if request.method== 'GET':
        if not task:
            return Response({"error":f"A task with id {pk} does not exist!"})
        else:
            serializer = TaskSerializer(task, many=False)
            return Response(serializer.data)
    elif request.method == 'POST':
        if not task:
            return Response({"error":f"A task with id {pk} does not exist!"})
        else:
            serializer = TaskSerializer(instance=task, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        if not task:
            return Response({"error":f"A task with id {pk} does not exist!"})
        else:
            task.delete()
            return Response({"Success":"Task successfully deleted!"})



