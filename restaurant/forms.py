from django import forms
from .models import Ingredient, Dish, Cook


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ("id",)
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(), widget=forms.CheckboxSelectMultiple
    )


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Dish
        fields = ("name", "dish_type", "description", "price", "ingredients")



class DishAssignCookForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects.filter(groups__name='Cook'),
        # widget=forms.CheckboxSelectMultiple
        widget=forms.RadioSelect,

    )

    class Meta:
        model = Dish
        fields = ['cooks']

    def clean(self):
        cleaned_data = super().clean()
        cooks = cleaned_data.get("cooks")
        if not cooks:
            raise forms.ValidationError("Please select at least one cook.")