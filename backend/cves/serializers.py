from rest_framework import serializers
from .models import CVE

class CVESerializer(serializers.ModelSerializer):
    class Meta:
        model = CVE
        fields = '__all__'