from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('exams', views.ExamViewSet)
router.register('items', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
