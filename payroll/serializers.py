from rest_framework import serializers
from .models import Payroll

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = [
            'id',
            'project',
            'name',
            'date_start',
            'date_end',
            'salary'
        ]