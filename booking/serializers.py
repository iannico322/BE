from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'start_date',
            'end_date',
            'activity_title',
            'requestor_name',
            'name',
            'contact_no',
            'email',
            'start_time',
            'end_time',
            'equipment',
            'status',
            'remarks',
            'attachment',
            'created_date',
            'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']