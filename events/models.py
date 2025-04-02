from django.db import models
from artist.models import Artist
from venue.models import Venue


class Event(models.Model):
    EVENT_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='events')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.venue.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # New event
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)