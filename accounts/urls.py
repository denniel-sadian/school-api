from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('employees', views.EmployeeProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register-employee-user/', views.CreateUserEmployeeView.as_view(), name='register')
]
