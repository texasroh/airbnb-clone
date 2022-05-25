from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView
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


def room_detail(request, pk):
    room = models.Room.objects.get(pk=pk)
    return render(request, "rooms/detail.html", {"room": room})
