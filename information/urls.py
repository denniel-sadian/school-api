from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('announcements', views.AnnouncementViewSet)
router.register('departments', views.DepartmentViewSet)
router.register('sections', views.SectionViewSet)
router.register('subjects', views.SubjectViewSet)
router.register('students', views.StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.SummaryView.as_view(), name='summary')
]
