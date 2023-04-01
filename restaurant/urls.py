from django.urls import path

from .views import index, CookListView, CookDetailView

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list",),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
]

app_name = "restaurant"
