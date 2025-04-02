from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from artist.models import Artist
from artist.serializers import ArtistSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class EventViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Retrieve a paginated list of published events.",
        responses={200: EventSerializer(many=True)}
    )
    def list(self, request):
        events = Event.objects.filter(status='published')
        paginator = StandardResultsSetPagination()
        events = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(events, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new event.",
        request_body=EventSerializer,
        responses={201: EventSerializer()}
    )
    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific event by ID.",
        responses={200: EventSerializer()}
    )
    def retrieve(self, request, pk=None):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update an event.",
        request_body=EventSerializer,
        responses={200: EventSerializer()}
    )
    def update(self, request, pk=None):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update an event.",
        request_body=EventSerializer,
        responses={200: EventSerializer()}
    )
    def partial_update(self, request, pk=None):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete an event.",
        responses={204: "No Content"}
    )
    def destroy(self, request, pk=None):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="List artists for a specific event.",
        responses={200: ArtistSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def artists_events(self, request, pk=None):
        event = get_object_or_404(Event.objects.all(), pk=pk)
        artists = Artist.objects.filter(events=event)
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
