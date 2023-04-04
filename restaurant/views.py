from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

from .forms import IngredientForm, DishForm, DishAssignCookForm
from .models import DishType, Dish, Cook, Ingredient


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
    context_object_name = 'cooks'
    template_name = 'restaurant/cook_list.html'
    paginate_by = 5


class CookDetailView(generic.DetailView):
    model = Cook
    # queryset = Cook.objects.all().prefetch_related("dish_set__dish_type")
    context_object_name = 'cook'
    template_name = 'restaurant/cook_detail.html'
    success_url = reverse_lazy("restaurant:cook-list")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = [
        'years_of_experience',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        "is_staff",
        "is_active",
        "is_superuser"
    ]
    template_name = 'restaurant/cook_form.html'
    success_url = reverse_lazy("restaurant:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ("username", "first_name", "last_name", "email",)
    success_url = reverse_lazy("restaurant:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    fields = "__all__"
    success_url = reverse_lazy("restaurant:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = 'dishes'
    template_name = 'restaurant/dish_list.html'
    paginate_by = 5


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'restaurant/dish_form.html'
    success_url = reverse_lazy("restaurant:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_form'] = IngredientForm()
        return context


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = "restaurant/dish_detail.html"
    success_url = reverse_lazy("restaurant:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assign_cook_form'] = DishAssignCookForm()
        context['all_cooks'] = Cook.objects.all()
        return context




class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant:dish-list")



class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dishtypes"
    template_name = 'restaurant/dishtype_list.html'
    paginate_by = 5


class DishTypeDetailView(generic.DetailView):
    model = DishType
    context_object_name = 'dish_type'
    template_name = 'restaurant/dishtype_detail.html'
    success_url = reverse_lazy("restaurant:dishtype_list")


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = 'restaurant/dishtype_form.html'
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

#
class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient
    template_name = 'restaurant/ingredient_detail.html'
    context_object_name = 'ingredient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient = context['ingredient']
        context['dishes'] = ingredient.dishes.all()
        return context


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("restaurant:ingredient-list")

class IngredientsForDishView(View):
    def get(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=kwargs['pk'])
        ingredients = dish.ingredients.all()
        context = {'dish': dish, 'ingredients': ingredients}
        return render(request, 'restaurant/dish_detail.html', context)


class DishAssignCookView(RedirectView):
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
                        request, f"{cook} has been removed from {dish.name}",
                        extra_tags="alert alert-danger"
                    )
                else:
                    dish.cooks.add(cook)
                    messages.success(
                        request, f"{cook} has been assigned to {dish.name}",
                        extra_tags="alert alert-success"
                    )
        else:
            messages.error(request, "No cook was selected")
        return super().post(request, *args, **kwargs)