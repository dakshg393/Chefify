from django.db import models
import uuid,os
from django.contrib.auth.models import User

from distutils import extension
from django.db.models import Avg



def recipe_image_path(instance, filename):
    # Split the filename to get the name and extension
    name, extension = os.path.splitext(filename)
    if not extension:
        raise ValueError("Filename must have an extension.")
    # Construct the filename as <recipe_id>.<extension>
    return f'recipe_images/{instance.recipe_id}{extension}'


def chefsImagePath(instance, filename):
    name, extension = os.path.splitext(filename)
    if not extension:
        raise ValueError("Filename must have an extension.")
    return f'chefs_images/{instance.chef_id}{extension}'



class Chefsprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chef_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chef_image = models.ImageField(upload_to=chefsImagePath, default='chefs_images/default_chef_image.jpg')
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    description=models.TextField(null=True)
    tags=models.CharField(max_length=100,null=True)
    


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chef=models.ForeignKey(Chefsprofile, on_delete=models.CASCADE)
    recipe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe_image = models.ImageField(upload_to=recipe_image_path, default='recipe_images/default_recipe_image.jpg')
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        average = RecipeRating.objects.filter(recipe=self).aggregate(Avg('rating'))
        return average['rating__avg'] or 0



class RecipeDetails(models.Model):
    recipeid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=50)
    total_time = models.IntegerField()
    difficulty = models.CharField(max_length=20)
    yields = models.IntegerField()
    cuisine = models.CharField(max_length=50)
    ingredients=models.CharField(max_length=50)
    



class RecipeSteps(models.Model):
    recipeid = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step1 = models.TextField(null=True)
    step2 = models.TextField(null=True)
    step3 = models.TextField(null=True)
    step4 = models.TextField(null=True)
    step5 = models.TextField(null=True)
    step6 = models.TextField(null=True)
    step7 = models.TextField(null=True)
    


class RecipeRating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(blank=True, null=True,default=n)
    comment = models.TextField(blank=True, null=True)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'recipe')

class RecipeFavourite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    
    class Meta:
        unique_together = ('user', 'recipe')