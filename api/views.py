from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view 

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