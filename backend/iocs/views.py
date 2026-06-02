from rest_framework import viewsets, permissions
from .models import IOC
from .serializers import IOCSerializer
from .filters import IOCFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class IOCViewSet(viewsets.ModelViewSet):
    queryset = IOC.objects.select_related('related_threat').all()
    serializer_class = IOCSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = IOCFilter
    search_fields = ['value', 'source']
    ordering_fields = ['first_seen', 'confidence']