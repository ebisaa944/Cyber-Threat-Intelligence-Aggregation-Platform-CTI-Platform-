from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from threats.models import Threat
from iocs.models import IOC
from cves.models import CVE
from datetime import timedelta, datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    # Totals
    total_threats = Threat.objects.count()
    total_iocs = IOC.objects.count()
    total_cves = CVE.objects.count()
    critical_cves = CVE.objects.filter(severity__iexact='CRITICAL').count()

    # Threat severity distribution
    severity = Threat.objects.values('severity').annotate(count=Count('id'))
    severity_map = {'critical':0, 'high':0, 'medium':0, 'low':0}
    for item in severity:
        severity_map[item['severity']] = item['count']

    # Top 5 sources
    sources = Threat.objects.values('source').annotate(count=Count('id')).order_by('-count')[:5]

    # Recent threats (last 30 days)
    recent = Threat.objects.filter(published_date__gte=datetime.utcnow()-timedelta(days=30)) \
                           .order_by('-published_date')[:10] \
                           .values('id', 'title', 'severity', 'source', 'published_date')

    # Daily trend (last 7 days)
    trend = Threat.objects.filter(published_date__gte=datetime.utcnow()-timedelta(days=7)) \
                          .annotate(date=TruncDate('published_date')) \
                          .values('date') \
                          .annotate(count=Count('id')) \
                          .order_by('date')

    return Response({
        'total_threats': total_threats,
        'total_iocs': total_iocs,
        'total_cves': total_cves,
        'critical_cves': critical_cves,
        'severity_distribution': severity_map,
        'top_sources': list(sources),
        'recent_threats': list(recent),
        'daily_trend': list(trend),
    })