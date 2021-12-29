from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,

)

from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('login/',views.loginUser, name='login'),
    path('register/',views.registerUser, name='register'),
    path('logout/',views.logoutUser, name='logout'),
    path('user/',views.getUser, name='user'),
    path('tasks/', views.tasksViews, name='tasks'),
    path('tasks/<str:pk>/', views.taskViews, name='task'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


