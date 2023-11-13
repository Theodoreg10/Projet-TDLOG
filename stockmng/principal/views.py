from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Product, Sale
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def handle_home_page(request):
    return render(request, "home.html")


@login_required(login_url='login')
def handle_data_page(request):
    products = Product.objects.all()
    sales = Sale.objects.all()
    products = Product.objects.all()
    context = {'products': products,
               'sales': sales
               }
    return render(request, "data.html", context)


def handle_about_page(request):
    return render(request, "about.html")


@login_required(login_url='login')
def handle_dashboard_page(request):
    return render(request, "dashboard.html")


def handle_login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('Accueil')
            else:
                error_message = "Invalid login credentials"
    else:
        form = LoginForm()
        error_message = None
    context = {'form': form, 'error_message': error_message}
    return render(request, "login.html", context)


def handle_logout_view(request):
    logout(request)
    return redirect('login')


def handle_register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Create a new user
            user = User.objects.create_user(
                username=name,
                password=password,
                email=email)

            # Log in the new user
            user = authenticate(request, username=name, password=password)
            login(request, user)

            return redirect('Accueil')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
