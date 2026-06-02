from rest_framework import viewsets, permissions
from .models import Threat
from .serializers import ThreatSerializer
from .filters import ThreatFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ThreatViewSet(viewsets.ModelViewSet):
    queryset = Threat.objects.all()
    serializer_class = ThreatSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ThreatFilter
    search_fields = ['title', 'description', 'source', 'threat_type']
    ordering_fields = ['published_date', 'created_at', 'severity']