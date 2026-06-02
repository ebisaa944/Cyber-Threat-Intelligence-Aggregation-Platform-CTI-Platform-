from django.db import models

class CVE(models.Model):
    cve_id = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    cvss_score = models.FloatField(null=True, blank=True)
    severity = models.CharField(max_length=20, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    exploit_available = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.cve_id