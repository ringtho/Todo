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