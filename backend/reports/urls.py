from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThreatReportViewSet

router = DefaultRouter()
# reports/urls.py
router.register(r'reports', ThreatReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]