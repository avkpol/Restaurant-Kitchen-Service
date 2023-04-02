from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import DishType, Dish, Cook


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dishtypes = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dishtypes": num_dishtypes,
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
    queryset = Cook.objects.all().prefetch_related("dish_set__dish_type")
    context_object_name = 'cooks'
    template_name = 'restaurant/cook_detail.html'
    success_url = reverse_lazy("restaurant:cook-list")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    fields = ['years_of_experience', 'username', 'email', 'password', 'first_name', 'last_name']
    template_name = 'restaurant/cook_form.html'
    success_url = reverse_lazy("restaurant:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ("username", "first_name", "last_name", "email",)
    success_url = reverse_lazy("restaurant:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = 'dishes'
    template_name = 'restaurant/dish_list.html'
    paginate_by = 5


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"
    template_name = 'restaurant/dish_form.html'
    success_url = reverse_lazy("restaurant:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    context_object_name = 'dishes'
    template_name = 'restaurant/dish_detail.html'
    success_url = reverse_lazy("restaurant:dish-list")


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


