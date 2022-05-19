from django.db import models
from core import models as core_models


class Reservation(core_models.TimeStampModel):
    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_COMFIRN = "confirm"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "pending"),
        (STATUS_COMFIRN, "confirm"),
        (STATUS_CANCELED, "canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"
