from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def log_page(request):
    return render (request, 'log_reg_page.html')

def register_user(request):
    if request.method == "POST":
        errors = Lead.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print(key, value)
            return redirect ('/')
        else:
            Lead.objects.register(request.POST)
            logged_user = Lead.objects.last()
            request.session['id'] = logged_user.id
            request.session['user'] = logged_user.first_name
            return redirect('/logged_in')

def log_in(request):
    result = Lead.objects.authenticate(request.POST['user_email'], request.POST['user_password'])
    if result == False:
        messages.error(request, "Invalid login Information")
        return redirect('/')
    if result == True:
        logged_user=Lead.objects.get(email=request.POST['user_email'])
        request.session['id'] = logged_user.id
        request.session['user'] = logged_user = logged_user.first_name
        return redirect('/home')

def logout(request):
    request.session.flush()
    return redirect ('/')

# PAGES
def home(request):
    if 'user' not in request.session:
        return redirect ('/')
    context={
        'logged_user':Lead.objects.get(id=request.session['id'])
    }
    return render (request, 'home_page.html', context)

# YOUR BAR PAGE AND FUNCTIONS
def your_bar(request):
    if 'user' not in request.session:
        return redirect('/') 
    context ={
        "bottles":Alcohol.objects.all()
    } #THIS CONTEXT MAY CHANGE BASED ON HOW MANY BARS HAVE LOG INS 
    return render(request, 'your_bar.html', context)

def add_alcohol(request):
    if request.method=="POST":
        errors = Alcohol.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print (key, value)
            return redirect('/your_bar')
        else:
            Alcohol.objects.add_alcohol(request.POST)
            return redirect('/your_bar')

def edit_alcohol(request,id):
    if 'user' not in request.session:
        return redirect('/')
    context={
        "this_alcohol" : Alcohol.objects.get(id=id)
    }
    return render(request, 'edit_alcohol.html', context)

def alcohol_edit_confirm(request, id):
    if request.method=="POST":
        errors = Alcohol.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print (key, value)
            return redirect(f'/edit_alcohol/{id}')
        else:
            this_bottle = Alcohol.objects.get(id=id)
            per_oz = (float(request.POST['cost']) / 25.3605)
            per_oz_round = round(per_oz, 2)
            this_bottle.brand = request.POST['brand']
            this_bottle.alcohol_type = request.POST['alcohol_type']
            this_bottle.cost = request.POST['cost']
            this_bottle.ppo = per_oz_round
            this_bottle.save()
        return redirect ('/your_bar')

def delete_alcohol(request, id):
    removed = Alcohol.objects.get(id=id)
    removed.delete()
    return redirect('/your_bar')

# CREATE COCKTAIL FUNTIONALITY
def codex(request):
    if 'user' not in request.session:
        return redirect('/') 
    context={
        "cocktails" : Cocktail.objects.all()
    }
    return render(request, 'codex.html', context)

def create_cocktail(request):
    if 'user' not in request.session:
        return redirect('/') 
    context={
        "alcohols" :Alcohol.objects.all()
    }
    return render(request, 'create_cocktail.html', context)

def cocktail_add(request):
    if request.method =='POST':
        errors = Cocktail.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print (key, value)
            return redirect('/create_cocktail')
        else:
            print(request.POST['quantity'])
            Cocktail.objects.add_cocktail(request.POST)
            Drink_Ingredient.objects.create(
                cocktail = Cocktail.objects.last(),
                liquor = Alcohol.objects.get(id=request.POST['liquor']),
                quantity = request.POST['quantity']
            )
            return redirect('/codex')

def edit_cocktail(request,id):
    if 'user' not in request.session:
        return redirect('/')
    context={
        "this_cocktail" : Cocktail.objects.get(id=id),
        "alcohols" :Alcohol.objects.all() 
    }
    return render(request, 'edit_cocktail.html', context)

def cocktail_edit_confirm(request, id):
    if request.method=="POST":
        errors = Cocktail.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                print (key, value)
            return redirect(f'/edit_cocktail/{id}')
        else:
            this_cocktail = Cocktail.objects.get(id=id)
            this_cocktail.name = request.POST['name']
            this_cocktail.desc = request.POST['desc']
            this_cocktail.save()
        return redirect ('/codex')

def delete_cocktail(request, id):
    removed = Cocktail.objects.get(id=id)
    removed.delete()
    return redirect('/codex')
