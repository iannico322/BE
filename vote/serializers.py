from rest_framework import serializers
from .models import Candidate

class CandidateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ['votes', 'voters']
    
    def get_image(self, obj):
        if obj.image:
            return obj.image.name
        return None
