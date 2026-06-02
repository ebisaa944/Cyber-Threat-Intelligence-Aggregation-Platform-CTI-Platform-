import django_filters
from .models import IOC

class IOCFilter(django_filters.FilterSet):
    ioc_type = django_filters.CharFilter(lookup_expr='iexact')
    confidence_min = django_filters.NumberFilter(field_name='confidence', lookup_expr='gte')
    source = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = IOC
        fields = ['ioc_type', 'source']