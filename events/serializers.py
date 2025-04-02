from django.utils import timezone
from rest_framework import serializers
from .models import Event
from artist.serializers import ArtistSerializer
from venue.serializers import VenueSerializer
from artist.models import Artist
from venue.models import Venue


class EventSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source='artist', write_only=True
    )
    venue_id = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all(), source='venue', write_only=True
    )

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['available_tickets', 'created_at', 'updated_at']

    def validate(self, data):
        if 'date_time' in data and data['date_time'] <= timezone.now():
            raise serializers.ValidationError("Event date must be in the future")

        if 'venue_id' in data and 'date_time' in data:
            venue = data['venue_id']
            date_time = data['date_time']
            conflicting_events = Event.objects.filter(
                venue=venue,
                date_time__date=date_time.date()
            ).exclude(pk=self.instance.pk if self.instance else None)

            if conflicting_events.exists():
                raise serializers.ValidationError("Venue is already booked for this date")

        return data