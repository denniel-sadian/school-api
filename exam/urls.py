from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('exams', views.ExamViewSet)
router.register('stripped-exams', views.StrippedExamViewSet, basename='stripped-exam')
router.register('items', views.ItemViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('sessions', views.StudentSessionViewSet, basename='session')
router.register('admincomments', views.AdminCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check/', views.CheckAnswers.as_view(), name='checking')
]
