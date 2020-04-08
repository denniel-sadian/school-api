from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('sheets', views.GradingSheetViewSet)
router.register('works', views.WorkViewSet)
router.register('records', views.RecordViewSet)

urlpatterns = [
    path('', include(router.urls))
]
