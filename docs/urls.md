## Urls
Contains the differents urls used in the application
is located at Projet-TDLOG/stockmng/principal/urls.py

### Dependencies
```python
from django.urls import path
from . import views
```

### urls

```python
urlpatterns = [
    path("", views.handle_home_page, name="Accueil"),                   # link by default to the home page
    path("accueil", views.handle_home_page, name="accueil"),            #link to home page
    path("data", views.handle_data_page, name="data"),                  # link to the data page
    path("about", views.handle_about_page, name="about"),               # link to the about page
    path("dashboard", views.handle_dashboard_page, name="dashboard"),   # link to the dashboard page
    path("login", views.handle_login_page, name="login"),               # link to login
    path("logout", views.handle_logout_view, name="logout"),            # urls to logout
    path("register", views.handle_register_page, name="register"),      # urls to register
    path("add_product", views.add_product, name="add_product"),         # url to add a product to the database
    path("add_sale", views.add_sale, name="add_sale"),                  # url to add a sale to the database
    path(                                                               # url to upload product from file
        "upload_product",
        views.handle_file_product_upload,
        name="upload_product"),
    path('get_product_details/<str:product_name>',                      # url to get information about a product given his name 
         views.get_product_details, name='get_product_details'),
    path("contact", views.handle_contact_page, name="contact"),         # link to the contact page
    path(
        "upload_sales",                                                 # url to upload sales from a file
        views.handle_file_sales_upload,
        name="upload_sales"),
    path("handle_scenario/<str:scenario>/<str:product_name>/<int:period>",  # url to get answer of sceanario handling given a product name a scenario and a period(year)
         views.handle_scenario,
         name="handle_scenario"),
    path('update_product/',                                              # url to update product information
         views.handle_update_product, name='update_product')
]

```
