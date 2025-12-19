from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'id',
            'proj_id',
            'name',
            'amount',
            'created_date'
        ]
        read_only_fields = ['id', 'created_date']