from django.urls import path
from . import views


urlpatterns = [
    path('', views.getTasks, name='tasks'),
    path('task/<str:pk>/', views.getTask, name="task"),
    path('create-task/', views.createTask, name='create-task')
]
