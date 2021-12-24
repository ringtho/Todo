from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Task
from . serializers import TaskSerializer 

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

@api_view(['GET'])
def getTasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTask(request, pk):
    task = Task.objects.get(id=pk)
    if task:
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)  
    else:
        return Response(f"The task with the id {pk} does not exist!")

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
