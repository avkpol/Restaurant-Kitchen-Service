from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View, generic
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import DishType, Dish, Cook


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "restaurant/index.html", context=context)


class CookListView(LoginRequiredMixin,generic.ListView):
    model = Cook
    context_object_name = 'cooks'
    template_name = 'cook_list.html'
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    context_object_name = 'cook'
    template_name = 'cook_detail.html'
    success_url = reverse_lazy("taxi:driver-list")