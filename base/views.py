from django.shortcuts import render
from django.http import HttpResponse
from . models import Task

def taskList(request):
    tasks = Task.objects.all()
    context = {"tasks":tasks}
    return render(request,'base/task_list.html', context)
