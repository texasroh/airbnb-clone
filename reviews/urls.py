from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:room_pk>", views.create_review, name="create"),
]
