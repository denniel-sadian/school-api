from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('departments', views.DepartmentViewSet)
router.register('sections', views.SectionViewSet)
router.register('subjects', views.SubjectViewSet)
router.register('students', views.StudentViewSet)
router.register('permissions', views.GuardianViewingPermissionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
