from rest_framework import serializers
from .models import Performer, JudgingCriteria

class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.photo:
            representation['photo'] = f"/media/{instance.photo.name}"
        return representation

class JudgingCriteriaSerializer(serializers.ModelSerializer):
    total_score = serializers.ReadOnlyField()
    
    class Meta:
        model = JudgingCriteria
        fields = '__all__'
        read_only_fields = ['total_score']
