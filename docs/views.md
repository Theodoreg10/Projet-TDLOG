## Views
### Dependencies
```python
# Django package
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Files imported
from .models import Product, Sale
from .forms import LoginForm, RegistrationForm, ProductForm, SaleForm
from .forms import FileUploadForm, ProductSelectionForm, ContactForm
from .forms import ScenarioForm


# packages created
from stock_package import django_to_df
import stock_package as st


# Other packages
import pandas as pd
import locale
from datetime import date
import numpy as np
import json
from pulp import (
    LpVariable, LpProblem, LpMinimize, LpBinary, lpSum, value, PULP_CBC_CMD
)
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
```
### functions
all the function name start by handle and then what the do
"""
Django views for handling various pages and scenarios in the application.
"""
#### function handle_home_page
Renders the home page.
Args:
    Request: Http Request.
Returns:
    The rendered home page.
```python
def handle_home_page(request):
    return render(request, "home.html")
```

#### function handle_data_page
Renders the data page for logged in users.
Shows products and sales related to the user and make sure that the user is autenticated
```python
@login_required(login_url="login")
def handle_data_page(request):
    products = Product.objects.filter(user=request.user)
    sales = Sale.objects.filter(user=request.user)
    form_product = ProductForm()
    form_sale = SaleForm(user=request.user)
    file_upload_form = FileUploadForm()
    context = {
        "products": products,
        "sales": sales,
        "form_product": form_product,
        "form_sale": form_sale,
        "file_upload_form": file_upload_form,
    }
    return render(request, "data.html", context)
```

#### function handle_about_page
Render the about page

#### function handle_dashboard_page
View function for handling the dashboard page.

Make sure the user is authenticated and render the dashboard with the product scelection form and the scenario scelection form

#### funcion handle_login_page
View function for the login page and handling login actions.
verify the user credential and send error message if necessary
```python
def handle_login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("Accueil")
            else:
                error_message = "Invalid login credentials"
                messages.error(request, 'Invalid login credentials')
    else:
        form = LoginForm()
        error_message = None
    context = {"form": form, "error_message": error_message}
    return render(request, "login.html", context)
```

#### function handle_logout_view
Logs the user out and redirects to the login page.

#### function handle_register_page
Render the registration page and is used to register a new user.

Verify if the usename and email already exist and send error message else create a new user and log in the user
```python
def handle_register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')  # or your view name
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')  # or your view name
            else:
                # Create a new user
                user = User.objects.create_user(
                    username=name, password=password, email=email
                )
                # Log in the new user
                user = authenticate(request, username=name, password=password)
                login(request, user)
                return redirect("Accueil")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})
```

#### function add_product
Adds a product and renders the data page.
add a product from the product forms and render the data page wth the new data

#### handle_update_product
Views function used to update information about a product in the sqlite database
```python
@csrf_exempt
def handle_update_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_name = data.get("product_name")
        qte_unitaire = data.get("qte_unitaire")
        unit_cost = data.get("unit_cost")
        fixed_command_cost = data.get("fixed_command_cost")
        holding_rate = data.get("holding_rate")
        service_level = data.get("service_level")
        try:
            product = Product.objects.get(
                product_name=product_name,
                user=request.user)
            product.qte_unitaire = qte_unitaire
            product.unit_cost = unit_cost
            product.fixed_command_cost = fixed_command_cost
            product.holding_rate = holding_rate
            product.service_level = service_level
            product.save()
            return JsonResponse({"status": "success"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error",
                                 "message": "Product does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error",
                             "message": "Invalid request method"})
```

#### function add_sale
Adds a sale with the SaleForm  and renders the data page.

#### function handle_file_product_upload
Handles file upload of product data and renders the data page.

Read the file and the data fron the file and try to add the information except for error.

#### function handle_file_sales_upload
Handles the download of sales data from a file uploaded by the user,
and updates the database.

#### function get_product_details
 Returns informations about the product in JSON format.
 These information are used in javascrip to display the selected product information in the dashboard page.

Args:
    request: The HTTP request object.
    product_name: The name of the product.

Returns:
    JsonResponse: JSON response containing product details.
    
```python
def get_product_details(request, product_name):
  try:
        product = Product.objects.get(product_name=product_name,
                                      user=request.user)
        return JsonResponse(
            {
                "product_name": product.product_name,
                "qte_unitaire": product.qte_unitaire,
                "unit_cost": str(product.unit_cost),
                "fixed_command_cost": str(product.fixed_command_cost),
                "holding_rate": str(product.holding_rate),
                "service_level": str(product.service_level),
            }
        )
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Product does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
```

#### function handle_contact_page
Handles the submission of the contact form and sends an email.

#### function handle_scenario
Main function of the apps render a json file containing information of the resust of the application of a scenario

Args : request,
      scenario: str equal scenario1, 2 3 or 4,
      product_name: name of the product we are applying the scenario to,
      period: The year of data we are working with. By default the actual year.
  
Result : jsonified data
##### result format
```python
data = {
            "date": list(inventory_data['month'].astype(str)),
            "month": list(sales_data_grouped["month"]),
            "quantité": list(sales_data_grouped["quantity"]),
            "stock_level": list(inventory_data["stock_level"]),
            "order": list(sales_data_grouped["order"]),
            "demand_all_product": list(completes_Sales["quantity"]),
            "product_names": list(completes_Sales["product_name"]),
            "command_cost": round(command_cost),
            "buying_cost": round(buying_cost),
            "inventory_cost": round(inventory_cost),
            "without_budget": round(command_cost + inventory_cost),
            "total_cost": round(command_cost + buying_cost + inventory_cost),
            "eoq": round(eoq, 1)
        }
```
