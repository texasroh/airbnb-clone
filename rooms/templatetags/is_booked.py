import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return False

    date = datetime.date(day.year, day.month, day.number)

    is_booked = reservation_models.BookedDay.objects.filter(
        day=date, reservation__room=room
    )

    return is_booked
