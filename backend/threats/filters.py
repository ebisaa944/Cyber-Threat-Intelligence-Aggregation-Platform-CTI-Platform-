import django_filters
from .models import Threat

class ThreatFilter(django_filters.FilterSet):
    severity = django_filters.CharFilter(lookup_expr='iexact')
    source = django_filters.CharFilter(lookup_expr='icontains')
    threat_type = django_filters.CharFilter(lookup_expr='icontains')
    date_from = django_filters.DateTimeFilter(field_name='published_date', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = Threat
        fields = ['severity', 'source', 'threat_type']