from django.urls import path
from . import views

urlpatterns = [
    path("", views.handle_home_page, name="Accueil"),
    path("accueil", views.handle_home_page, name="accueil"),
    path("data", views.handle_data_page, name="data"),
    path("about", views.handle_about_page, name="about"),
    path("dashboard", views.handle_dashboard_page, name="dashboard"),
]
