from django.contrib import admin
from .models import Recipe,RecipeDetails,RecipeSteps,RecipeRating,Chefsprofile,RecipeFavourite

admin.site.register(Recipe)
admin.site.register(RecipeDetails)
admin.site.register(RecipeSteps)
admin.site.register(RecipeRating)
admin.site.register(Chefsprofile)
admin.site.register(RecipeFavourite)