
from django.contrib.auth import login as dj_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

from .forms import (
    LoginForm,
    RegisterForm,
    CookSearchForm,
    DishForm,
    DishAssignCookForm,
    DishSearchForm,
    DishTypeSearchForm,
    IngredientSearchForm,
)

from .models import DishType, Dish, Cook, Ingredient


def login(request):
    """View function for the register page of the site."""
    context = {"login": LoginForm()}
    return render(request, "registration/login.html", context=context)


def sign_up(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "registration/register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            dj_login(request, user)
            return redirect("restaurant:login")
        else:
            return render(request, "registration/register.html", {"reg_form": form})


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dishtypes = DishType.objects.count()
    num_ingredients = Ingredient.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dishtypes": num_dishtypes,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits + 1,
    }

    return render(request, "restaurant/index.html", context=context)


class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cooks"
    template_name = "restaurant/cook_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = CookSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(username__icontains=name)
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    context_object_name = "cook"
    template_name = "restaurant/cook_detail.html"
    success_url = reverse_lazy("restaurant:cook-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dishes"] = Dish.objects.filter(cooks=self.object)
        return context


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = [
        "years_of_experience",
        "username",
        "email",
        "password",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
    ]
    template_name = "restaurant/cook_form.html"
    success_url = reverse_lazy("restaurant:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("restaurant:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("restaurant:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "restaurant/dish_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DishSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "restaurant/dish_form.html"
    success_url = reverse_lazy("restaurant:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_dish_types"] = DishType.objects.all()
        return context


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "restaurant/dish_detail.html"
    success_url = reverse_lazy("restaurant:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assign_cook_form"] = DishAssignCookForm()
        context["all_cooks"] = Cook.objects.all()
        return context


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("restaurant:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant:dish-list")


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dishtypes"
    template_name = "restaurant/dishtype_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DishTypeSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "restaurant/dishtype_detail.html"
    success_url = reverse_lazy("restaurant:dishtype_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dishes"] = Dish.objects.filter(dish_type=self.object)
        return context


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "restaurant/dishtype_form.html"
    success_url = reverse_lazy("restaurant:dishtype-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("restaurant:dishtype-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("restaurant:dishtype-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    context_object_name = "ingredients"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = IngredientSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    template_name = "restaurant/ingredient_detail.html"
    context_object_name = "ingredient"


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("restaurant:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("restaurant:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("restaurant:ingredient-list")


class IngredientsForDishView(View):
    def get(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=kwargs["pk"])
        ingredients = dish.ingredients.all()
        context = {"dish": dish, "ingredients": ingredients}
        return render(request, "restaurant/dish_detail.html", context)


class DishAssignCookView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("restaurant:dish-list")

    def post(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=self.kwargs["pk"])
        cook_id = request.POST.get("cook_id")
        if cook_id:
            try:
                cook = Cook.objects.get(pk=cook_id)
            except Cook.DoesNotExist:
                messages.error(request, "Selected cook does not exist")
            else:
                if cook in dish.cooks.all():
                    dish.cooks.remove(cook)
                    messages.success(
                        request,
                        f"Cook {cook} no more responsible for {dish.name}",
                        extra_tags="alert alert-danger",
                    )
                else:
                    dish.cooks.add(cook)
                    messages.success(
                        request,
                        f"{dish.name} has been assigned to cook {cook} ",
                        extra_tags="alert alert-success",
                    )
        else:
            messages.error(request, "No cook was selected")
        return super().post(request, *args, **kwargs)
