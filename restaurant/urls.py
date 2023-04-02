from django.urls import path

from .views import (
    index,
    CookListView,
    CookDetailView,
    CookCreateView,
    CookUpdateView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishDeleteView,
    DishTypeListView,
    DishTypeCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookListView.as_view(), name="cook-list",),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create", CookCreateView.as_view(), name="cook-form"),
    path("cooks/<int:pk>/update", CookUpdateView.as_view(), name="cook-form"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    # path("dishes/<int:pk>/update", DishUpdateView.as_view(), name="dish-detail"),
    path("dishes/create", DishCreateView.as_view(), name="dish-form"),
    path("dishes/<int:pk>/delete", DishDeleteView.as_view(), name="dish-delete"),
    path("dish_types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish_types/create", DishTypeCreateView.as_view(), name="dish-type-form"),
]

app_name = "restaurant"
