from multiprocessing import BoundedSemaphore
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django_countries import countries

# from django.core.paginator import Paginator, EmptyPage
# from django.utils import timezone
from . import models


# def all_rooms(request):
#     page_num = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         page = paginator.page(page_num)
#     except EmptyPage:
#         # page = paginator.page(1)
#         return redirect("/")
#     # page = paginator.get_page(page_num)
#     return render(
#         request,
#         "rooms/home.html",
#         {"page": page},
#     )


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans: int = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # now = timezone.now()
        # context["now"] = now
        return context


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#     except models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         raise Http404()
#     return render(request, "rooms/detail.html", {"room": room})


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    model = models.Room


def search(request):
    city = request.GET.get("city", "")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    instant = request.GET.get("instant", False)
    superhost = request.GET.get("superhost", False)

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city:
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price > 0:
        filter_args["price__lte"] = price

    if guests > 0:
        filter_args["guests__gte"] = guests

    if bedrooms > 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds > 0:
        filter_args["beds__gte"] = beds
    if baths > 0:
        filter_args["baths__gte"] = baths

    if instant:
        filter_args["instant_book"] = True

    if superhost:
        filter_args["host__superhost"] = True

    if s_amenities:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = s_amenity

    if s_facilities:
        for s_facility in s_facilities:
            filter_args["facilitires__pk"] = s_facility

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )
