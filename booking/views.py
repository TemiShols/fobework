from decimal import Decimal
from django.db.models import F
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookingViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all bookings for the current user.",
        responses={200: BookingSerializer(many=True)}
    )
    def list(self, request):
        bookings = Booking.objects.filter(user=request.user)
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(bookings, request)
        serializer = BookingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific booking.",
        responses={200: BookingSerializer()}
    )
    def retrieve(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)  # Only owner or admin can view booking details
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to view this booking."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new booking.",
        request_body=BookingSerializer,
        responses={201: BookingSerializer()}
    )
    def create(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                event = serializer.validated_data['event']
                tickets = int(serializer.validated_data['tickets'])

                # Check ticket availability
                if tickets > event.available_tickets:
                    return Response(
                        {"error": "Not enough tickets available"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                total_amount = Decimal(tickets) * event.ticket_price

                # Atomically update available tickets also Event.objects.filter(getting it dynamically)
                event.__class__.objects.filter(pk=event.pk).update(
                    available_tickets=F('available_tickets') - tickets
                )

                booking = serializer.save(
                    user=request.user,
                    total_amount=total_amount
                )

                return Response(
                    BookingSerializer(booking).data,
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update booking status (admin only).",
        request_body=BookingSerializer,
        responses={200: BookingSerializer()}
    )
    def update(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)  # Only admin can update booking status
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin can update booking status."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Cancel a booking.",
        responses={204: "No Content"}
    )
    def destroy(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)  # Only owner, booker or admin can cancel
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN
            )

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Get booking receipt.",
        responses={200: "Receipt data"}
    )
    @action(detail=True, methods=['get'])
    def receipt(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)  # Only owner, booker or admin can view receipt
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to view this receipt."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate receipt data
        receipt_data = {
            "booking_id": booking.id,
            "event": booking.event.title,
            "user": booking.user.username,
            "tickets": booking.tickets,
            "total_amount": str(booking.total_amount),
            "payment_status": booking.payment_status,
            "payment_method": booking.payment_method,
            "transaction_id": booking.transaction_id,
            "booking_date": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        return Response(receipt_data)
