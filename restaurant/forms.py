from django import forms
from .models import Ingredient, Dish, Cook, DishType


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ("id",)
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all()
    )

    class Meta:
        model = Dish
        fields = (
            "name",
            "dish_type",
            "description",
            "price",
            "ingredients"
        )



class DishAssignCookForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects.all(),
        # queryset=Cook.objects.filter(groups__name='Cook'),
        # widget=forms.RadioSelect,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = ['cooks']

    def clean(self):
        cleaned_data = super().clean()
        cooks = cleaned_data.get("cooks")
        if not cooks:
            raise forms.ValidationError(
                "Please select at least one cook."
            )


class CookSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by username:"}
        ),
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by dish name:"}
        ),
    )

class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by dish type name:"}
        ),
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by ingredient name:"}
        ),
    )