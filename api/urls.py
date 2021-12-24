from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('tasks/', views.getTasks),
    path('tasks/<str:pk>/', views.getTask),
    path('tasks-create/',views.createTask),
    path('tasks-update/<str:pk>/',views.updateTask),
    path('tasks-delete/<str:pk>/',views.deleteTask),
]


