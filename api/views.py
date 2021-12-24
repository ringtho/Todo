from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def getTasks(request):
    routes = [
        'GET /api/tasks',
        'GET /api/tasks/:id',

    ]
    return JsonResponse(routes,safe=False)