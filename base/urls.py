from django.urls import path
from . import views


urlpatterns = [
    path('', views.getTasks, name='tasks'),
    path('task/<str:pk>/', views.getTask, name="task"),
    path('task-create/', views.createTask, name='create-task'),
    path('task-update/<str:pk>/', views.updateTask, name='update-task'),
    path('task-delete/<str:pk>', views.deleteTask, name="delete-task"),
]
