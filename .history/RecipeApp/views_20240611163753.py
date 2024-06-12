import email
from email import message
from unicodedata import category
from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User 
from .forms import RecipeForm,RecipeDetailsForm,RecipeStepsForm,RecipeRatingForm,ChefsprofileForm
from .models import Recipe,RecipeDetails,RecipeSteps,Chefsprofile,RecipeRating,RecipeFavourite

from faker import Faker


def index(request):


    return render(request,'index.html')


# def Recipespage(request):
    if request.user.is_authenticated:
        
        sort_by = request.GET.get('sort')
        
        if sort_by == 'new_to_old':
            sort_value = '-created_at'
        elif sort_by == 'old_to_new':
            sort_value = 'created_at'
        elif sort_by == 'rating_low_to_high':
            sort_value = 'total_time'
        elif sort_by == 'rating_high_to_low':
            sort_value = '-total_time'
        elif sort_by == 'time_low_to_high':
            sort_value = 'total_time'
        elif sort_by == 'time_high_to_low':
            sort_value = '-total_time'
        else:
            sort_value = '-created_at'  # Default sorting

        # Initialize recipe queryset
        recipes = Recipe.objects.all()
        allrecipes = recipes.order_by(sort_value)
        is_favorited = RecipeFavourite.objects.filter(user=request.user, recipe=recipe, like=True).exists()

        allrecipesWithReating= []
        for recipe in allrecipes:
            allrecipesWithReating.append({'recipe': recipe, 'average_rating': recipe.average_rating(),'is_favorited':is_favorited,})
          
        heading = "Result: All Recipes"

        if request.method == "POST":
            category = request.POST.getlist('category')
            time = request.POST.get('time')
            difficulty = request.POST.get('difficulty')
            
            filter_conditions = {}

            if category:
                filter_conditions['category__in'] = category

            if time:
                filter_conditions['total_time'] = time

            if difficulty:
                filter_conditions['difficulty'] = difficulty

            
            
            recipelist = RecipeDetails.objects.filter(**filter_conditions).values_list('recipeid', flat=True)
            recipelist = list(recipelist)
            recipes = Recipe.objects.filter(recipe_id__in=recipelist)

        # Apply sorting to the filtered queryset
            allrecipes = recipes.order_by(sort_value)
            allrecipesWithReating= []
            is_favorited = RecipeFavourite.objects.filter(user=request.user, recipe=recipe, like=True).exists()

            for recipe in allrecipes:
                allrecipesWithReating.append({'recipe': recipe, 'average_rating': recipe.average_rating(),'is_favorited': is_favorited,})
            heading = f"Filter: ({recipe.count()} Recipes)"
        
        

        return render(request, 'recipes.html', {'allrecipesWithReating': allrecipesWithReating, 'heading': heading})
    else:
        messages.info(request, 'please login to see recipe page')
        return redirect('loginpage')


def Recipespage(request):
    if request.user.is_authenticated:
        sort_by = request.GET.get('sort')
        
        if sort_by == 'new_to_old':
            sort_value = '-created_at'
        elif sort_by == 'old_to_new':
            sort_value = 'created_at'
        elif sort_by == 'rating_low_to_high':
            sort_value = 'average_rating'
        elif sort_by == 'rating_high_to_low':
            sort_value = '-average_rating'
        elif sort_by == 'time_low_to_high':
            sort_value = 'total_time'
        elif sort_by == 'time_high_to_low':
            sort_value = '-total_time'
        else:
            sort_value = '-created_at'  # Default sorting

        # Initialize recipe queryset
        recipes = Recipe.objects.all()
        allrecipes = recipes.order_by(sort_value)
        allrecipesWithReating = []

        for recipe in allrecipes:
            is_favorited = RecipeFavourite.objects.filter(user=request.user, recipe=recipe, like=True).exists()
            allrecipesWithReating.append({
                'recipe': recipe,
                'average_rating': recipe.average_rating(),
                'is_favorited': is_favorited,
            })

        heading = "Result: All Recipes"

        if request.method == "POST":
            category = request.POST.getlist('category')
            time = request.POST.get('time')
            difficulty = request.POST.get('difficulty')
            
            filter_conditions = {}

            if category:
                filter_conditions['category__in'] = category

            if time:
                filter_conditions['total_time'] = time

            if difficulty:
                filter_conditions['difficulty'] = difficulty

            recipelist = RecipeDetails.objects.filter(**filter_conditions).values_list('recipeid', flat=True)
            recipelist = list(recipelist)
            recipes = Recipe.objects.filter(recipe_id__in=recipelist)  # Use id__in instead of recipe_id__in

            # Apply sorting to the filtered queryset
            allrecipes = recipes.order_by(sort_value)
            allrecipesWithReating = []

            for recipe in allrecipes:
                is_favorited = RecipeFavourite.objects.filter(user=request.user, recipe=recipe, like=True).exists()
                allrecipesWithReating.append({
                    'recipe': recipe,
                    'average_rating': recipe.average_rating(),
                    'is_favorited': is_favorited,
                })

            heading = f"Filter: ({recipes.count()} Recipes)"

        
        return render(request, 'recipes.html', {'allrecipesWithReating': allrecipesWithReating, 'heading': heading})
    else:
        return render(request, 'login.html')


def Occasionspage(request):
    return HttpResponse("this is about page")


def aboutpage(request):
        
    return render(request, 'about.html')




def loginpage(request):

    if request.user.is_authenticated:
        
        messages.info(request, 'You are already logged in.')
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')



def signuppage(request):

    if request.user.is_authenticated:
        
        messages.info(request, 'You are already logged in.')
        return redirect('/Recipes/')
    else:
        return render(request, 'signup.html')


def createrecipeform(request):

    if request.user.is_authenticated: 
        if Chefsprofile.objects.filter(user=request.user).exists(): 

            return render(request, 'createrecipe.html')
        else:
            messages.info(request, 'You are not register as a chef \n Please Register As a Chef')
            return redirect('/chefregisterform/') 
    else:
        messages.info(request, 'You are not Login \n Please login First')
        return render(request, 'login.html')


def chefregisterform(request):
    if request.user.is_authenticated:
        
        if Chefsprofile.objects.filter(user=request.user).exists(): 

            messages.info(request, 'Chefs Account Alredy created You are alredy register as a Chef')
            return redirect('/Recipes/')
        
        else:
            return render(request,'chefregister.html')
    
    else:
        return redirect('/login/')


def signup_request(request):

        if request.method == "POST" :
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('/signup/')

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('/signup/')
    
            user = User.objects.create(
                first_name = first_name,
                last_name =last_name,
                username = username,
                email =email,
                        )
            user.set_password(password)
            user.save()

            messages.info(request, 'User successfully Register!')

            return render(request,'signup.html')


        return render(request,'signup.html')


def login_request(request):
    
        if request.method == "POST" :
            username = request.POST.get('username')
            password = request.POST.get('password')


            if not User.objects.filter(username = username).exists():
                messages.info(request, 'Username not found Please Register')
                return redirect('/signup/')
            

            user = authenticate(request, username=username , password=password)

            if user is None:
                messages.info(request, 'Incorrect password')
                return redirect('/login/')
            
            else:
                login(request,user)
               
                return redirect('/Recipes/')
            
            
            
        return render(request,'login.html')


def logout_request(request):
    logout(request)

    request.session.flush()

    return redirect('/login/')


def chefregister(request):
    if request.method == "POST":
     
        chefform = ChefsprofileForm(request.POST, request.FILES)
        if chefform.is_valid():
            chef=chefform.save(commit=False)
            chef.user = request.user
            
            chef.save()

            messages.info(request, 'Chefs Account created Successfully \n Now You Can Create Recipe')
            return redirect('/createrecipeform/')
        else:
            
            messages.error(request, 'Somthing Went Wrong in Form Data')  
            return render(request, 'chefregister.html')
    else:
        messages.error(request, 'Somthing Went Wrong Please Try Again')  
        return render(request, 'chefregister.html')
    




def createrecipe(request):

    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)
        details_form = RecipeDetailsForm(request.POST)
        steps_form = RecipeStepsForm(request.POST)

  
        if recipe_form.is_valid() and details_form.is_valid() and steps_form.is_valid():
            
            # Associate the authenticated user with the recipe
            recipe = recipe_form.save(commit=False)
            

            recipe.user = request.user
            recipe.chef = Chefsprofile.objects.get(user=request.user)
            recipe.save()

            details = details_form.save(commit=False)
            details.recipeid = recipe
            details.save()

            steps = steps_form.save(commit=False)
            steps.recipeid = recipe
            steps.save()

            messages.info(request, 'Recipe created Successfully')
            return redirect('/Recipes/') # Assuming 'recipes' is the correct URL name
        else:
            # Form is invalid, re-render the form with error messages
            print("Form errors:", recipe_form.errors)
            messages.error(request, 'Recipe not created. Something went wrong.')
            return redirect('/Recipes/')
    else:
        messages.error(request, 'somthing went wrong')
        return render(request,'recipes.html')
    

def recipe_detail(request, pk):
    # Retrieve the recipe object using recipe_id
    if request.user.is_authenticated:
        recipe = Recipe.objects.get(recipe_id=pk)
    
        recipe_detail = RecipeDetails.objects.get(recipeid=pk)
    
        recipe_steps = RecipeSteps.objects.get(recipeid=pk)

        ingredients_list = recipe_detail.ingredients.split(',')

        ratings= RecipeRating.objects.get(recipe=pk)

        return render(request, 'recipe_detail.html', {'recipe': recipe, 'recipe_detail': recipe_detail, 'recipe_steps': recipe_steps , 'ingredients_list': ingredients_list,'rating':rating})
    
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')
  


def Chefspage(request):
    if request.user.is_authenticated:
        chefs = Chefsprofile.objects.all()
        return render(request, 'chefs.html', {'chefs': chefs})
       
        # return render(request, 'recipes.html')
    else:
        messages.info(request, 'please login to see chefs page')
        return redirect('loginpage')
    

def chefs_profile(request, username):

    if request.user.is_authenticated:

        chef = get_object_or_404(User, username=username)
        # Filter recipes by the fetched user
        recipe = Recipe.objects.filter(user=chef).order_by('-created_at')
        chefdetails=Chefsprofile.objects.get(username=chef)
        
        return render(request, 'chefsprofile.html', {'recipe': recipe, 'chefdetails':chefdetails })
       
        # return render(request, 'recipes.html')
    else:
        messages.info(request, 'please login to see recipe page')
        return redirect('loginpage')

  


def add_favorite(request, recipe_id):
    if not request.user.is_authenticated:
        message.info(request,"You are not login Please Login")
        return redirect('loginpage')
    else:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        favorite, created = RecipeFavourite.objects.get_or_create(user=request.user, recipe=recipe)
        favorite.like = not favorite.like
        favorite.save()

        
        return redirect('/Recipes/')






















































def fakedate(n):
        for i in range(n):
        

            fake = Faker("en_IN")
            username1=fake.first_name()
            email1=fake.email()

            user= User.objects.create(
                first_name = username1,
                last_name =fake.last_name(),
                username = username1,
                email =email1,
            )

            user.set_password("123456")

            user.save()

def show():
    user = User.objects.values_list('username', flat=True)
    return list(user)


def aa():

    a= Chefsprofile.objects.create(
  
        name = "username",       
        username = "rname",
        description="fgdgd",
        tags="jdkj,ddf"
        
    )

    

    a.save()


