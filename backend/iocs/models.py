from django.db import models
from threats.models import Threat

class IOC(models.Model):
    IOC_TYPES = [
        ('ip', 'IP Address'),
        ('domain', 'Domain'),
        ('url', 'URL'),
        ('hash', 'Hash'),
        ('email', 'Email'),
    ]
    ioc_type = models.CharField(max_length=20, choices=IOC_TYPES)
    value = models.CharField(max_length=500)
    confidence = models.IntegerField(default=50)
    source = models.CharField(max_length=100)
    first_seen = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    related_threat = models.ForeignKey(Threat, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ['ioc_type', 'value']
        ordering = ['-first_seen']

    def __str__(self):
        return f"{self.ioc_type}:{self.value}"