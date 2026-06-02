from rest_framework import viewsets, permissions
from .models import ThreatReport
from .serializers import ThreatReportSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
import io

class ThreatReportViewSet(viewsets.ModelViewSet):
    serializer_class = ThreatReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin/staff users may view all reports; regular users only their own
        user = self.request.user
        if user and user.is_authenticated and (user.is_staff or user.is_superuser):
            return ThreatReport.objects.all()
        return ThreatReport.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        report = self.get_object()
        buffer = io.BytesIO()
        try:
            # Import reportlab lazily to avoid failing tests when not installed
            from reportlab.pdfgen import canvas
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
        except Exception:
            # Fallback: return a simple text response wrapped as application/pdf
            txt = f"Report: {report.title}\nBy: {report.created_by.username}\n\n{report.summary}"
            buffer.write(txt.encode('utf-8'))
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=f'report_{report.id}.pdf', content_type='application/pdf')