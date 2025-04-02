from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from .models import Venue
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.pagination import PageNumberPagination
from .serializers import VenueSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class VenueViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        operation_summary="Retrieve a list of all venues with optional filtering.",
        responses={200: VenueSerializer(many=True)}
    )
    def list(self, request):
        venues = Venue.objects.all()
        city = request.query_params.get('city', None)
        if city:
            venues = venues.filter(city__iexact=city)

        country = request.query_params.get('country', None)
        if country:
            venues = venues.filter(country__iexact=country)

        min_capacity = request.query_params.get('min_capacity', None)
        if min_capacity:
            venues = venues.filter(capacity__gte=min_capacity)

        amenity = request.query_params.get('amenity', None)
        if amenity:
            venues = venues.filter(amenities__contains=[amenity])

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(venues, request)
        serializer = VenueSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific venue.",
        responses={200: VenueSerializer()}
    )
    def retrieve(self, request, pk=None):
        venue = get_object_or_404(Venue, pk=pk)
        serializer = VenueSerializer(venue)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new venue.",
        request_body=VenueSerializer,
        responses={201: VenueSerializer()}
    )
    def create(self, request):
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update all fields of a venue.",
        request_body=VenueSerializer,
        responses={200: VenueSerializer()}
    )
    def update(self, request, pk=None):
        venue = get_object_or_404(Venue, pk=pk)
        if venue.owner != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update a venue.",
        request_body=VenueSerializer,
        responses={200: VenueSerializer()}
    )
    def partial_update(self, request, pk=None):
        venue = get_object_or_404(Venue, pk=pk)

        # Check if user is owner or admin
        if venue.owner != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = VenueSerializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a venue.",
        responses={204: "No Content"}
    )
    def destroy(self, request, pk=None):
        venue = get_object_or_404(Venue, pk=pk)

        # Check if user is owner or admin
        if venue.owner != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Retrieve all events for a specific venue.",
        responses={200: EventSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        venue = get_object_or_404(Venue, pk=pk)
        events = Event.objects.filter(venue=venue)
        status = request.query_params.get('status', None)
        if status:
            events = events.filter(status=status)

        date = request.query_params.get('date', None)
        if date:
            events = events.filter(date_time__date=date)

        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)