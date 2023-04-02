from django.urls import path

from .views import (
    index,
    CookListView,
    CookDetailView,
    CookCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list",),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create", CookCreateView.as_view(), name="cook-form"),
]

app_name = "restaurant"
