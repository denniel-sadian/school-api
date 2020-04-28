from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('sheets', views.GradingSheetViewSet)
router.register('works', views.WorkViewSet)
router.register('records', views.RecordViewSet)
router.register('cards', views.CardViewSet)
router.register('permissions', views.ViewingPermissionViewSet)
router.register('finalgrades', views.FinalGradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('multiple-records/', views.MultipleRecordCreateView.as_view(), name='multiple-records'),
    path('write-grades/', views.WriteGradesToCardsView.as_view(), name='write-grades')
]
