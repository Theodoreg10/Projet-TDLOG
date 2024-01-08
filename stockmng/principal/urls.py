from django.urls import path
from . import views

urlpatterns = [
    path("", views.handle_home_page, name="Accueil"),
    path("accueil", views.handle_home_page, name="accueil"),
    path("data", views.handle_data_page, name="data"),
    path("about", views.handle_about_page, name="about"),
    path("dashboard", views.handle_dashboard_page, name="dashboard"),
    path("login", views.handle_login_page, name="login"),
    path("logout", views.handle_logout_view, name="logout"),
    path("register", views.handle_register_page, name="register"),
    path("add_product", views.add_product, name="add_product"),
    path("add_sale", views.add_sale, name="add_sale"),
    path("upload_product", views.handle_file_upload, name="upload_product"),
    path(
        "get_product_details/<str:product_name>",
        views.get_product_details,
        name="get_product_details",
    ),
]
