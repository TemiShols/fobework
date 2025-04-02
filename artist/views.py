from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Artist
from rest_framework.pagination import PageNumberPagination
from .serializers import ArtistSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArtistViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Get a list of all artists",
        responses={200: ArtistSerializer(many=True)}
    )
    def list(self, request):
        artists = Artist.objects.all()
        paginator = StandardResultsSetPagination()
        artists = paginator.paginate_queryset(artists, request)
        serializer = ArtistSerializer(artists, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get a specific artist by ID",
        responses={
            200: ArtistSerializer(),
            404: "Artist not found"
        }
    )
    def retrieve(self, request, pk=None):
        queryset = Artist.objects.all()
        artist = get_object_or_404(queryset, pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new artist profile",
        request_body=ArtistSerializer,
        responses={
            201: ArtistSerializer(),
            400: "Invalid data"
        }
    )
    def create(self, request):
        # Associate with the logged-in user
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update an artist profile completely",
        request_body=ArtistSerializer,
        responses={
            200: ArtistSerializer(),
            400: "Invalid data",
            403: "Permission denied",
            404: "Artist not found"
        }
    )
    def update(self, request, pk=None):
        artist = get_object_or_404(Artist, pk=pk)

        # Check if the user owns this artist profile
        if artist.user != request.user:
            return Response({"detail": "You do not have permission to edit this artist profile."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update an artist profile",
        request_body=ArtistSerializer,
        responses={
            200: ArtistSerializer(),
            400: "Invalid data",
            403: "Permission denied",
            404: "Artist not found"
        }
    )
    def partial_update(self, request, pk=None):
        artist = get_object_or_404(Artist, pk=pk)

        # Check if the user owns this artist profile
        if artist.user != request.user:
            return Response({"detail": "You do not have permission to edit this artist profile."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ArtistSerializer(artist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete an artist profile",
        responses={
            204: "No content - deleted successfully",
            403: "Permission denied",
            404: "Artist not found"
        }
    )
    def destroy(self, request, pk=None):
        artist = get_object_or_404(Artist, pk=pk)

        # Check if the user owns this artist profile
        if artist.user != request.user:
            return Response({"detail": "You do not have permission to delete this artist profile."},
                            status=status.HTTP_403_FORBIDDEN)

        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Get the logged-in user's artist profile",
        responses={
            200: ArtistSerializer(),
            404: "Artist profile not found"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):  # Get the logged-in user's artist profile
        try:
            artist = Artist.objects.get(user=request.user)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist:
            return Response(
                {"detail": "You don't have an artist profile yet."},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_summary="Verify an artist (admin only)",
        responses={
            200: ArtistSerializer(),
            404: "Artist not found"
        }
    )
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):  # Admin action to verify an artist
        artist = get_object_or_404(Artist, pk=pk)
        artist.is_verified = True
        artist.save()
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
