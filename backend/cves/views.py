from rest_framework import viewsets, permissions
from .models import CVE
from .serializers import CVESerializer
from rest_framework.filters import SearchFilter, OrderingFilter

class CVEViewSet(viewsets.ModelViewSet):
    queryset = CVE.objects.all()
    serializer_class = CVESerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['cve_id', 'description']
    ordering_fields = ['published_date', 'cvss_score']