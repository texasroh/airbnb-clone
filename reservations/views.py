import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


def create(request, room_pk, year, month, day):
    try:
        date_obj = datetime.date(year, month, day)
        room_obj = room_models.Room.objects.get(pk=room_pk)
        models.BookedDay.objects.get(
            # day=date_obj,
            day__range=(date_obj, date_obj + datetime.timedelta(days=1)),
            reservation__room=room_obj,
        )
        messages.error(request, "That day is already booked")
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    except room_models.Room.DoesNotExist:
        messages.error(request, "Room does not exist")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room_obj,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()

        form = review_forms.CreateReviewForm()

        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()

    if verb == "confirm" and reservation.room.host == request.user:
        reservation.status = models.Reservation.STATUS_COMFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation__pk=reservation.pk).delete()

    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
