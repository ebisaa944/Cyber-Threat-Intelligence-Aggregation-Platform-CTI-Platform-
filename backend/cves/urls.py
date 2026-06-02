from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CVEViewSet

router = DefaultRouter()
router.register(r'cves', CVEViewSet)

urlpatterns = [
    path('', include(router.urls)),
]