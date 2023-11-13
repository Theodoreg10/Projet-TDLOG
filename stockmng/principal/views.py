from django.shortcuts import render
from .models import Product, Sale

# Create your views here.


def handle_home_page(request):
    return render(request, "home.html")


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


def handle_dashboard_page(request):
    return render(request, "dashboard.html")
