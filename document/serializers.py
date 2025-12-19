from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    template = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'name',
            'status',
            'date_created',
            'last_modified',
            'created_by',
            'submitted_by',
            'template',
            'document_data',
            'assignatures',
            'remarks',
            'department',
            'tracking_id',
            'to_route',
            'isupload',
            'uploadedFile'
        ]
        read_only_fields = ['id', 'date_created', 'last_modified', 'tracking_id']
    
    def get_template(self, obj):
        if obj.template:
            return {
                "id": obj.template.id,
                "name": obj.template.name,
                "body": obj.template.body,
                "file": obj.template.file
            }
        return None