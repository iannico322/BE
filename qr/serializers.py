from rest_framework import serializers
from .models import QR

class QRSerializer(serializers.ModelSerializer):
    class Meta:
        model = QR
        fields = [
            'id',
            'name',
            'email',
            'designation',
            'lgu_agency',
            'created_date'
        ]
        read_only_fields = ['id', 'created_date']