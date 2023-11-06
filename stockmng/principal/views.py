from django.shortcuts import render

# Create your views here.


def handle_home_page(request):
    return render(request, "home.html")


def handle_data_page(request):
    return render(request, "data.html")


def handle_about_page(request):
    return render(request, "about.html")


def handle_dashboard_page(request):
    return render(request, "dashboard.html")
