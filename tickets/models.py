from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from air_zone.models import Flight


class Order(models.Model):
    """
    Model to hold information about the user orders.
    """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class Ticket(models.Model):
    """
    Model to hold information about the tickets.
    """
    row = models.IntegerField()
    seat = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['row', 'seat', 'flight'], name='unique_ticket'),
        ]

    def clean(self):
        if not self.flight:
            raise ValidationError({'flight': 'Flight must be provided before saving ticket.'})

        airplane = self.flight.airplane
        if not airplane:
            raise ValidationError({'flight': 'This flight has no airplane assigned.'})

        if not (1 <= self.row <= airplane.rows and 1 <= self.seat <= airplane.seats):
            raise ValidationError({'row': 'Seat or row number is not valid for this airplane.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket ({self.row}-{self.seat}) for flight {self.flight.id}"
