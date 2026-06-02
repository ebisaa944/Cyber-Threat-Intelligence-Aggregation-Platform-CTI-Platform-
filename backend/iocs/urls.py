from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IOCViewSet

router = DefaultRouter()
router.register(r'iocs', IOCViewSet)

urlpatterns = [
    path('', include(router.urls)),
]