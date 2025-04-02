from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_countries.serializer_fields import CountryField


class CustomUserSerializer(serializers.ModelSerializer):
    country = CountryField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'last_login',
            'date_created',
            'is_active',
            'state',
            'city',
            'country',
            'telephone',
        ]
        read_only_fields = ['last_login', 'date_created', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'company_name', 'state', 'city', 'country', 'telephone']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if needed (these will be in the token payload)
        # token['name'] = user.name
        # token['is_admin'] = user.is_admin

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_id'] = user.id
        data['email'] = user.email

        return data
