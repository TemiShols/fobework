from django.db import models
from events.models import Event
from django.conf import settings
from decimal import Decimal


class Booking(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    tickets = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} for {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.pk:  # New booking
            tickets_int = int(self.tickets)
            self.total_amount = Decimal(tickets_int) * self.event.ticket_price
            self.event.available_tickets -= self.tickets
            self.event.save()
        super().save(*args, **kwargs)