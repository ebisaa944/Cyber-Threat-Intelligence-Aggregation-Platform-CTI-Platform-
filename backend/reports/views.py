from rest_framework import viewsets, permissions
from .models import ThreatReport
from .serializers import ThreatReportSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas

class ThreatReportViewSet(viewsets.ModelViewSet):
    serializer_class = ThreatReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ThreatReport.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        report = self.get_object()
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Report: {report.title}")
        p.drawString(100, 780, f"By: {report.created_by.username}")
        p.drawString(100, 760, f"Date: {report.created_at.strftime('%Y-%m-%d')}")
        y = 740
        for line in report.summary.split('\n'):
            p.drawString(100, y, line[:100])
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'report_{report.id}.pdf')