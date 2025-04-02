from rest_framework import serializers
from .models import Venue
from authentication.serializers import CustomUserSerializer


class VenueSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['amenities'] = instance.amenities or []
        representation['photos'] = instance.photos or []
        return representation
