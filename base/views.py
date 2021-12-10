from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from . models import Task
from . forms import MyUserCreationForm, TaskForm


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
            messages.success(request,"User successfully logged in!")
            return redirect('tasks')
        else:
            messages.error(request, "Incorrect Username or Password")
        
    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    messages.success(request,"User successfully logged out!")
    return redirect('login')

def registerUser(request):
    form = MyUserCreationForm()
    if request.user.is_authenticated:
        return redirect('tasks')
    if request.method=="POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, "An error occured during the registration. Please Try again")
    context = {'form': form}
    return render(request, 'base/register.html', context)

@login_required(login_url='/login')
def getTasks(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    user_tasks = Task.objects.filter(user=request.user)
    tasks = user_tasks.filter(Q(title__startswith=q))
    incomplete_tasks = user_tasks.filter(complete=False)
    count = incomplete_tasks.count
    context = {"tasks":tasks, "count": count}
    return render(request,'base/task_list.html', context)

@login_required(login_url='/login')
def getTask(request,pk):
    task = Task.objects.get(id=pk)
    context = {"task": task}
    return render(request, 'base/task.html', context)

@login_required(login_url='/login')
def createTask(request):
    form = TaskForm()
    if request.method=="POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('tasks')
    context = {'form': form}
    return render(request,'base/task_form.html', context)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')
    context = {'task':task}
    return render(request, 'base/delete.html', context)
