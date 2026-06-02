from django.db import models
from authentication.models import User

class ThreatReport(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return self.title