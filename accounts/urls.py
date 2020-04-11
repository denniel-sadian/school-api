from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('permissions', views.AccountCreationPermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.CreateUserProfileView.as_view(), name='register'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path('change-dp/', views.ChangePhotoView.as_view(),
         name='change-dp')
]
