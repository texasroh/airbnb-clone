from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    page_num = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    page = paginator.get_page(page_num)
    return render(
        request,
        "rooms/home.html",
        {"page": page},
    )
