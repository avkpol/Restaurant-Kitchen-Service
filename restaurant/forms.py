from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Ingredient, Dish, Cook, DishType


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    dish_type = forms.ModelChoiceField(queryset=DishType.objects.all())

    class Meta:
        model = Dish
        fields = ("name", "dish_type", "description", "price", "ingredients")


class DishAssignCookForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects.all(),
      )

    class Meta:
        model = Dish
        fields = ["cooks"]

    def clean(self):
        cleaned_data = super().clean()
        cooks = cleaned_data.get("cooks")
        if not cooks:
            raise forms.ValidationError("Please select at least one cook.")


class CookSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username:"}),
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by dish name:"}),
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by dish type name:"}),
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by ingredient name:"}),
    )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Cook
        fields = ["username", "email", "password1", "password2"]
