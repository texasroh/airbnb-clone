from django.views.generic import ListView, DetailView, View
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django_countries import countries
from django.core.paginator import Paginator


# from django.core.paginator import Paginator, EmptyPage
# from django.utils import timezone
from . import models, forms


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
    paginate_by = 12
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


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city:
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type:
                    filter_args["room_type"] = room_type

                if price:
                    filter_args["price__lte"] = price

                if guests:
                    filter_args["guests__gte"] = guests

                if bedrooms:
                    filter_args["bedrooms__gte"] = bedrooms
                if beds:
                    filter_args["beds__gte"] = beds
                if baths:
                    filter_args["baths__gte"] = baths

                if instant_book:
                    filter_args["instant_book"] = True

                if superhost:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilitires"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )

        else:
            form = forms.SearchForm()

        return render(
            request,
            "rooms/search.html",
            {"form": form},
        )


# def search(request):

#     country = request.GET.get("country")

#     if country:
#         form = forms.SearchForm(request.GET)
#         if form.is_valid():
#             city = form.cleaned_data.get("city")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guests = form.cleaned_data.get("guests")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             beds = form.cleaned_data.get("beds")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             facilities = form.cleaned_data.get("facilities")

#             filter_args = {}

#             if city:
#                 filter_args["city__startswith"] = city

#             filter_args["country"] = country

#             if room_type:
#                 filter_args["room_type"] = room_type

#             if price:
#                 filter_args["price__lte"] = price

#             if guests:
#                 filter_args["guests__gte"] = guests

#             if bedrooms:
#                 filter_args["bedrooms__gte"] = bedrooms
#             if beds:
#                 filter_args["beds__gte"] = beds
#             if baths:
#                 filter_args["baths__gte"] = baths

#             if instant_book:
#                 filter_args["instant_book"] = True

#             if superhost:
#                 filter_args["host__superhost"] = True

#             for amenity in amenities:
#                 filter_args["amenities"] = amenity

#             for facility in facilities:
#                 filter_args["facilitires"] = facility

#             rooms = models.Room.objects.filter(**filter_args)

#     else:
#         form = forms.SearchForm()

#     return render(
#         request,
#         "rooms/search.html",
#         {"form": form, "rooms": rooms},
#     )
