from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'url', 'description', 'date_created', 'date_updated', 'tags']
        read_only_fields = ['id', 'date_created', 'date_updated']