    
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from ProductManagement.models import Category, Product
from UserManagement.forms import ConsumerRegistrationForm, ConsumerLoginForm
from UserManagement.models import Consumer
# Create your views here.

def home(request,cat):
    context = {
        "cat":cat,
        'products':  Product.objects.order_by('-ccscore').filter(category__name=cat),
        "categories": Category.objects.all()
    }
    if request.user.is_authenticated:
        context['consumer']= Consumer.objects.get(username=request.user.username)
    return render(request, 'home.html',context)

def register(request):
    if request.method == 'POST':
        form = ConsumerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home','Laptop')
    else:
        form = ConsumerRegistrationForm()
    if request.user.is_authenticated:
        return render(request, 'register.html', {'form': form, "consumer":Consumer.objects.get(username=request.user.username)})
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = ConsumerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home',"Laptop")
    else:
        form = ConsumerLoginForm()
    if request.user.is_authenticated:
        return render(request, 'login.html', {'form': form, "consumer":Consumer.objects.get(username=request.user.username),"categories":Category.objects.all()})
    return render(request, 'login.html', {'form': form,"categories":Category.objects.all()})

def logout_view(request):
    logout(request)
    return redirect('home',"Laptop")


