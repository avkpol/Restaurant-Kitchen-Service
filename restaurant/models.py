from django.db import models
from django.contrib.auth.models import AbstractUser


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    dish_type = models.CharField(max_length=100)
    cooks = models.ManyToManyField(Cook, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='DishIngredient', related_name='dishes'
    )

    def __str__(self):
        return self.name

    @property
    def available_cooks(self):
        return Cook.objects.exclude(pk__in=self.cooks.all().values_list('pk', flat=True))


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

