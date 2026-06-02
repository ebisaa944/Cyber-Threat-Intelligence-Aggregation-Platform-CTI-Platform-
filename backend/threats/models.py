from django.db import models

class Threat(models.Model):
    SEVERITY = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY, default='medium')
    threat_type = models.CharField(max_length=100, blank=True)
    external_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title