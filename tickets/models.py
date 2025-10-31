from django.db import models
from django.contrib.auth import get_user_model
from air_zone.models import Flight


class Order(models.Model):
    """
    Model to hold information about the user order's.
    """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)


class Ticket(models.Model):
    """
    Model to hold information about the tickets.
    """
    row = models.IntegerField()
    seat = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['row', 'seat', 'flight'], name='unique_ticket'),
        ]

    def clean(self):
        # Chack that row and seat values is able
        if not (
            1 <= self.row <= airplane.rows
            and
            1 <= self.seat <= airplane.seats
        ):
            raise ValidationError(
                {'row': 'Seat or row is not able.'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
