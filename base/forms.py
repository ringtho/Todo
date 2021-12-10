from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Task


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','complete']

