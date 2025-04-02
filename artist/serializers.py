from rest_framework import serializers
from .models import Artist
from authentication.serializers import CustomUserSerializer


class ArtistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genres'] = instance.genres or []
        representation['social_media'] = instance.social_media or []
        representation['portfolio_links'] = instance.portfolio_links or []
        return representation
