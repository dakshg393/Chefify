from django.contrib import admin
from django.urls import path


from RecipeApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('Recipes/', views.Recipespage, name='Recipespage'),  # Added trailing slash
    path('Chefs/', views.Chefspage, name='Chefspage'),  # Added trailing slash# Added trailing slash
    path('about/', views.aboutpage, name='aboutpage'),  # Added trailing slash
    path('signup/', views.signuppage, name='signuppage'),  # Added trailing slash
    path('login/', views.loginpage, name='loginpage'),  # Added trailing slash
    path('recipe/<uuid:pk>/', views.recipe_detail, name='recipe_detail'),
    path('chefs_profile/<str:username>/', views.chefs_profile, name='chefs_profile'),
    path('createrecipeform/', views.createrecipeform, name='createrecipeform'),
    path('chefregisterform/', views.chefregisterform, name='chefregisterform'),
    path('chefregister/', views.chefregister, name='chefregister'), 
    path('add_favorite/<uuid:recipe_id>/', views.add_favorite, name='add_favorite'),
    # the html page redirect on url page using url name 
    # for actions
    path('register/', views.signup_request, name='signup'), 
    path('signin/', views.login_request, name='signin'),
    path('logout/', views.logout_request, name='logout'),
    path('createrecipe/', views.createrecipe, name='createrecipe'),
   
]





