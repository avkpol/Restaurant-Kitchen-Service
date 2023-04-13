from django.urls import path

from .views import (
    index,
    login,
    sign_up,
    CookListView,
    CookDetailView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    DishTypeListView,
    DishTypeDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    DishAssignCookView,
    IngredientListView,
    IngredientCreateView,
    IngredientsForDishView,
    IngredientDetailView,
    IngredientUpdateView,
    IngredientDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("register/", sign_up, name="register"),
    path("login/", login, name="login"),
    # path('logout/', log_out, name='logout'),
    # path('register/', sign_up, name='register'),
    path(
        "cooks/",
        CookListView.as_view(),
        name="cook-list",
    ),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cooks/create", CookCreateView.as_view(), name="cook-form"),
    path("cooks/<int:pk>/update", CookUpdateView.as_view(), name="cook-form"),
    path("cooks/<int:pk>/delete", CookDeleteView.as_view(), name="cook-confirm-delete"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update", DishUpdateView.as_view(), name="dish-form"),
    path("dishes/create", DishCreateView.as_view(), name="dish-form"),
    path(
        "dishes/<int:pk>/delete", DishDeleteView.as_view(), name="dish-confirm-delete"
    ),
    path("dishtypes/", DishTypeListView.as_view(), name="dishtype-list"),
    path("dishtypes/<int:pk>/", DishTypeDetailView.as_view(), name="dishtype-detail"),
    path("dishtypes/create", DishTypeCreateView.as_view(), name="dishtype-form"),
    path(
        "dishtypes/<int:pk>/delete",
        DishTypeDeleteView.as_view(),
        name="dishtype-confirm-delete",
    ),
    path(
        "dishtypes/<int:pk>/update", DishTypeUpdateView.as_view(), name="dishtype-form"
    ),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/create", IngredientCreateView.as_view(), name="ingredient-form"),
    path(
        "ingredients/<int:pk>", IngredientDetailView.as_view(), name="ingredient-detail"
    ),
    path(
        "ingredients/<int:pk>/update",
        IngredientUpdateView.as_view(),
        name="ingredient-form",
    ),
    path(
        "ingredients/<int:pk>/delete",
        IngredientDeleteView.as_view(),
        name="ingredient-confirm-delete",
    ),
    path(
        "dishes/<int:pk>/ingredients/",
        IngredientsForDishView.as_view(),
        name="ingredients-for-dish",
    ),
    path(
        "dishes/<int:pk>/assign-me/",
        DishAssignCookView.as_view(),
        name="dish-assign-cook",
    ),
]

app_name = "restaurant"
