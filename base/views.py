from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import Task
from . forms import TaskForm


def loginView(request):
    if request.user.is_authenticated:
        return redirect('tasks')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            username = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, "Incorrect Username or Password")
        
    return render(request, 'base/login.html')


def getTasks(request):
    tasks = Task.objects.all()
    context = {"tasks":tasks}
    return render(request,'base/task_list.html', context)

def getTask(request,pk):
    task = Task.objects.get(id=pk)
    context = {"task": task}
    return render(request, 'base/task.html', context)

def createTask(request):
    form = TaskForm()
    if request.method=="POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    context = {'form': form}
    return render(request,'base/task_form.html', context)

def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method=="POST":
        form = TaskForm(request.POST, instance=task)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        if request.POST.get('complete') is None:
            task.complete = False
        else:
            task.complete = True
        task.save()
        return redirect('tasks')
    context = {"form":form}
    return render(request, 'base/task_form.html', context)

def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')
    context = {'task':task}
    return render(request, 'base/delete.html', context)
