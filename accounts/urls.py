from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('permissions', views.AccountCreationPermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.CreateUserProfileView.as_view(), name='register')
]
