from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.CreateUserEmployeeView.as_view(), name='register'),
]
