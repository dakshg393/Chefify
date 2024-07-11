
from traceback import print_tb
from unicodedata import category
from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from grpc import Status
from numpy import average 
from .forms import RecipeForm,RecipeDetailsForm,RecipeStepsForm,RecipeRatingForm,ChefsprofileForm,ChefRatingForm
from .models import Recipe,RecipeDetails,RecipeSteps,Chefsprofile,RecipeRating,RecipeFavourite,ChefRating
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Avg,Q


def index(request):

    chefs = Chefsprofile.objects.all()
    allchefsWithReating = []

    for chef in chefs:
        allchefsWithReating.append({
            'chef': chef,
            'average_rating': chef.average_rating(),
        })

    # top_chefs = sorted(allchefsWithReating, key=lambda x: x['average_rating'], reverse=True)[:5]
    top_chefs = sorted(allchefsWithReating, key=lambda x: x['average_rating'] if x['average_rating'] is not None else float('-inf'), reverse=True)[:5]

    
    recipes = Recipe.objects.all()

    allrecipesWithReating = []


    
    for recipe in recipes:
        
        if request.user.is_authenticated:
            is_favorited = RecipeFavourite.objects.filter(user=request.user, recipe=recipe, like=True).exists()
        
        else:
            is_favorited =False
        

        allrecipesWithReating.append({
            'recipe': recipe,
            'average_rating': recipe.average_rating(),
            'is_favorited': is_favorited,
        })

    # top_recipes =sorted(allrecipesWithReating, key=lambda x:x['average_rating'], reverse=True)[:3]
    top_recipes = sorted(allrecipesWithReating, key=lambda x: x['average_rating'] if x['average_rating'] is not None else float('-inf'), reverse=True)[:3]

    
    return render(request,'index.html',{'top_chefs': top_chefs , 'top_recipes':top_recipes })



def Recipespage(request):
    if request.user.is_authenticated:
        sort_by = request.GET.get('sort')
        print(sort_by)
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

        categ = request.GET.getlist('category')

        if request.method == "POST" or categ:
            if request.method == "POST":
                category = request.POST.getlist('category')
                print(category)
            else:
                category= categ
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


        page = request.GET.get('page', 1)
        paginator = Paginator(allrecipesWithReating, 9)  # Show 10 recipes per page

        try:
            allrecipesWithReating = paginator.page(page)
        except PageNotAnInteger:
            allrecipesWithReating = paginator.page(1)
        except EmptyPage:
            allrecipesWithReating = paginator.page(paginator.num_pages)
   

        
        return render(request, 'recipes.html', {'allrecipesWithReating': allrecipesWithReating, 'heading': heading})
    else:
        return render(request, 'login.html')


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

        ratings= RecipeRating.objects.filter(recipe=pk)



        if request.method == 'POST':
            form = RecipeRatingForm(request.POST)
            if form.is_valid():
                if not RecipeRating.objects.filter(user=request.user, recipe=recipe).exists():
                
                    feedback =form.save(commit=False)
                    feedback.user=request.user
                    feedback.recipe = recipe 
                    feedback.save()
                    
                    return redirect('recipe_detail', pk=pk)
                else:
                    messages.error(request, 'You alredy give review for this recipe')
                    
        else:
            form = RecipeRatingForm()

        return render(request, 'recipe_detail.html', {'recipe': recipe, 'recipe_detail': recipe_detail, 'recipe_steps': recipe_steps , 'ingredients_list': ingredients_list,'ratings':ratings})
    
    else:
        messages.info(request, 'Please Login First')
        return render(request, 'login.html')
  


def Chefspage(request):
    if request.user.is_authenticated:
        chefs = Chefsprofile.objects.all()
        allchefsWithReating = []

        for chef in chefs:
            allchefsWithReating.append({
                'chef': chef,
                'average_rating': chef.average_rating(),
            })

        return render(request, 'chefs.html', {'allchefsWithReating': allchefsWithReating})
    else:
        messages.info(request, 'Please login to see chefs page')
        return redirect('loginpage')

def chefs_profile(request, username):

    if request.user.is_authenticated:

        if request.method == 'POST':
            form_type = request.POST.get('form_type')
                
            if form_type == 'rating_form':
                form = ChefRatingForm(request.POST)
                if form.is_valid():
                    chef_profile = get_object_or_404(Chefsprofile, user__username=username)
                    
                    # Check if a ChefRating object already exists for the current user and chef profile
                    chefrating, created = ChefRating.objects.get_or_create(
                        user=request.user,
                        chef=chef_profile,
                        defaults={'rating': form.cleaned_data['rating']}  # Update with the relevant field names from your form
                    )
                    
                    if not created:
                        # Update the existing ChefRating object if it already exists
                        chefrating.rating = form.cleaned_data['rating']  # Update with the relevant field names from your form
                        chefrating.save()
                        print("Update successful")
                    else:
                        print("Save successful")  # This line assumes you wanted to print this message if a new object is created

                    
 

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
        chef = get_object_or_404(User, username=username)
        chefdetails=Chefsprofile.objects.get(username=chef)
        recipes = Recipe.objects.filter(user=chef)
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


        page = request.GET.get('page', 1)
        paginator = Paginator(allrecipesWithReating, 9)  # Show 10 recipes per page

        try:
            allrecipesWithReating = paginator.page(page)
        except PageNotAnInteger:
            allrecipesWithReating = paginator.page(1)
        except EmptyPage:
            allrecipesWithReating = paginator.page(paginator.num_pages)
   
        try:
            rating = ChefRating.objects.get(chef=username, user=request.user)
        except ObjectDoesNotExist:
            rating = None


        return render(request, 'chefsprofile.html', {'allrecipesWithReating': allrecipesWithReating, 'heading': heading, 'chefrating':rating , 'chefdetails':chefdetails })
       
        
    else:
        messages.info(request, 'please login to see recipe page')
        return redirect('loginpage')

  



def add_favorite(request, recipe_id):
    if not request.user.is_authenticated:
        messages.info(request, "You are not logged in. Please log in.")
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    favorite, created = RecipeFavourite.objects.get_or_create(user=request.user, recipe=recipe)
    favorite.like = not favorite.like
    favorite.save()

    return JsonResponse({'status': 'success', 'is_favorited': favorite.like})



def removeRecipe(request , recipeid):
    if not request.user.is_authenticated:
        messages.info(request,"User is not loggin please login first")
        return JsonResponse({'status' : 'error', 'message':'user us not login'} , status=401)
    
    recipe = get_object_or_404(Recipe, pk=recipeid)
    recipe.delete()

    return JsonResponse({'status':'success'})









def get_suggestions(request):
    query = request.GET.get('query', '')
    if len(query) > 3:
        # Fetch suggestions from Recipe and Chef models
        recipes = Recipe.objects.filter(title__icontains=query)[:5].values( 'title','recipe_id','recipe_image')
        chefs = Chefsprofile.objects.filter(name__icontains=query)[:5].values( 'name','chef_image','username')
        
        # Convert QuerySets to lists
        recipes_list = list(recipes)
        chefs_list = list(chefs)
        
        # Return JsonResponse with serialized data
        return JsonResponse({'recipes': recipes_list, 'chefs': chefs_list}, safe=False)
    else:
        return JsonResponse({'recipes': [], 'chefs': []})


































