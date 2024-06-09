from django import forms
from .models import Recipe,RecipeDetails,RecipeSteps,RecipeRating,Chefsprofile

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'recipe_image']

class RecipeDetailsForm(forms.ModelForm):
    class Meta:
        model = RecipeDetails
        fields = ['description', 'category', 'total_time', 'difficulty', 'yields', 'cuisine','ingredients']

class RecipeStepsForm(forms.ModelForm):
    class Meta:
        model = RecipeSteps
        fields = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6', 'step7']


class RecipeRatingForm(forms.ModelForm):
    class Meta:
        model = RecipeRating
        fields = ['rating','comment','like']


class ChefsprofileForm(forms.ModelForm):
    class Meta:
        model = Chefsprofile
        fields = ['chef_image', 'name', 'username', 'description', 'tags']

