from rest_framework import serializers
from events.models import Event
from .models import Booking
from events.serializers import EventSerializer
from authentication.serializers import CustomUserSerializer


class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source='event', write_only=True
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['total_amount', 'created_at', 'updated_at']