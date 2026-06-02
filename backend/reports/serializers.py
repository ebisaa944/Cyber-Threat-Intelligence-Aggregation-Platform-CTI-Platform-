from rest_framework import serializers
from .models import ThreatReport

class ThreatReportSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = ThreatReport
        fields = ['id', 'title', 'summary', 'created_by', 'created_by_username', 'created_at', 'pdf_file']
        read_only_fields = ['created_by', 'created_at']