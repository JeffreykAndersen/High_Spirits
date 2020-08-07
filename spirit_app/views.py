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

def delete_alcohol(request, id):
    removed = Alcohol.objects.get(id=id)
    removed.delete()
    return redirect('/your_bar')

def create_cocktail(request):
    if 'user' not in request.session:
        return redirect('/') 
    return render(request, "create_cocktail.html")