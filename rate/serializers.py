from rest_framework import serializers
from .models import Performer, JudgingCriteria

class PerformerSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model = Performer
        fields = '__all__'
    
    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name
        return None

class JudgingCriteriaSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    
    class Meta:
        model = JudgingCriteria
        fields = '__all__'
        read_only_fields = ['total_score']
