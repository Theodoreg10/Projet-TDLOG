"""
Django views for handling various pages and scenarios in the application.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Product, Sale
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, ProductForm, SaleForm
from .forms import FileUploadForm, ProductSelectionForm, ContactForm
from .forms import ScenarioForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from stock_package import django_to_df
import stock_package as st
from datetime import date
import numpy as np
import json


# Create your views here.


def handle_home_page(request):
    """
    Renders the home page.

    Args:
        Request: Http Request.

    Returns:
        The rendered home page.
    """
    return render(request, "home.html")


@login_required(login_url='login')
def handle_data_page(request):
    """
    Renders the data page for logged in users. Shows products and sales related to the user.

    Args:
        Request: Http Request.

    Returns:
        Rendered data page containing products, sales, and forms.
    """
    products = Product.objects.filter(user=request.user)
    sales = Sale.objects.filter(user=request.user)
    form_product = ProductForm()
    form_sale = SaleForm(user=request.user)
    file_upload_form = FileUploadForm()
    context = {'products': products,
               'sales': sales,
               'form_product': form_product,
               'form_sale': form_sale,
               'file_upload_form': file_upload_form
               }
    return render(request, "data.html", context)


def handle_about_page(request):
    return render(request, "about.html")


@login_required(login_url='login')
def handle_dashboard_page(request):
    """
    View function for handling the dashboard page.

    Args:
        Request: Http Request.

    Returns:
        Rendered dashboard page.
    """
    product_selection_form = ProductSelectionForm()
    scenario_form = ScenarioForm()
    context = {
        'product_selection_form': product_selection_form,
        'scenario_form': scenario_form
    }
    return render(request, "dashboard.html", context)


def handle_login_page(request):
    """
    View function for the login page and handling login actions.

    Args:
        Request: Http Request.

    Returns:
        Rendered login page.
    """
  
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
    """
    Logs the user out and redirects to the login page.

    Args:
        Request: Http Request.

    Returns:
        Redirected login page.
    """

    logout(request)
    return redirect('login')


def handle_register_page(request):
    """
    Renders the registration page and handles user registration.

    Args:
        Request: Http Request.

    Returns:
        Rendered registration page.
    """
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


@login_required(login_url='login')
def add_product(request):
    """
    Adds a product and renders the data page.

    Args:
        Request: Http Request.

    Returns:
        Rendered data page.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('data')
    else:
        sale_form = SaleForm(user=request.user)
        product_form = ProductForm()
        context = {
            'form_sale': sale_form,
            'form_product': product_form
        }
    return render(request, 'data.html', context)

@csrf_exempt
def handle_update_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('product_name')
        qte_unitaire = data.get('qte_unitaire')
        unit_cost = data.get('unit_cost')
        fixed_command_cost = data.get('fixed_command_cost')
        holding_rate = data.get('holding_rate')
        service_level = data.get('service_level')

        product = Product.objects.get(name=product_name)
        product.qte_unitaire = qte_unitaire
        product.unit_cost = unit_cost
        product.fixed_command_cost = fixed_command_cost
        product.holding_rate = holding_rate
        product.service_level = service_level
        product.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

@login_required(login_url='login')
def add_sale(request):
    """
    Adds a sale and renders the data page.

    Args:
        Request: Http Request.

    Returns:
        Rendered data page.
    """
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            return redirect('data')
    else:
        sale_form = SaleForm(user=request.user)
        product_form = ProductForm()
        context = {
            'form_sale': sale_form,
            'form_product': product_form
        }
    return render(request, 'data.html', context)


def handle_file_product_upload(request):
    """
    Handles file upload of product data and renders the data page.

    Args:
        Request: Http Request.

    Returns:
        Rendered data page.
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                df = pd.read_csv(file, sep=';')
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)

            for _, row in df.iterrows():
                Product.objects.create(
                    product_name=row['Product name'],
                    qte_unitaire=row['Qte unitaire'],
                    unit_cost=row['Unit cost'],
                    fixed_command_cost=row['Fixed command cost'],
                    holding_rate=row['Holding rate'],
                    service_level=row['Service level'],
                    user=request.user
                )
            return redirect('data')
    else:
        form = FileUploadForm()
    return render(request, 'data.html', {'form': form})


@login_required(login_url='login')
def handle_file_sales_upload(request):
    """
    Handles the download of sales data from a file uploaded by the user, and updates the database.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'data' page upon successful upload.
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                df = pd.read_csv(file, sep=";")
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            for _, row in df.iterrows():
                product = Product.objects.get(product_name=row['Ref'],
                                              user=request.user)
                Sale.objects.create(
                    date=row['Date'],
                    quantity=row['Quantity'],
                    ref=product,
                    user=request.user
                )
            return redirect('data')
    else:
        form = FileUploadForm()
    return render(request, 'data.html', {'form': form})

def get_product_details(request, product_name):
<<<<<<< HEAD
    """
    Returns product details in JSON format.

    Args:
        request: The HTTP request object.
        product_name: The name of the product.

    Returns:
        JsonResponse: JSON response containing product details.
    """
    product = Product.objects.get(product_name=product_name)
=======
    product = Product.objects.get(product_name=product_name, user=request.user)
>>>>>>> 311c758786f5a48941a672c7a916a16c85c1b217
    return JsonResponse({
        'product_name': product.product_name,
        'qte_unitaire': product.qte_unitaire,
        'unit_cost': str(product.unit_cost),
        'fixed_command_cost': str(product.fixed_command_cost),
        'holding_rate': str(product.holding_rate),
        'service_level': str(product.service_level),
    })

@login_required(login_url='login')
def handle_contact_page(request):
    """
    Handles the submission of the contact form and sends an email.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'contact' page upon successful form submission.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                'Contact Form Submission',  # subject
                form.cleaned_data['message'],  # message
                form.cleaned_data['email'],  # from email
                ['theodoregnimavo6@gmail.com'],  # to email
            )
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'contact_form': form})

def handle_scenario(request):
    """
    Handles a scenario by querying product and sales data, and displaying DataFrames.

    Args:
        request: The HTTP request object.
    """
    products_query = Product.objects.all()
    sales_query = Sale.objects.all()
    products_dataframe = django_to_df(products_query)
    sales_dataframe = django_to_df(sales_query)

    # Display DataFrames
    print("Products DataFrame:")
    print(products_dataframe)

    print("\nSales DataFrame:")
    print(sales_dataframe)

def handle_scenario1(request, product_name):
    """
    Handles scenario 1 by returning sales data for a specific product in JSON format.

    Args:
        request: The HTTP request object.
        product_name: The name of the product.

    Returns:
        JsonResponse: JSON response containing sales data.
    """
    sales_data = django_to_df(Sale, product=product_name, is_product=False)
    if sales_data is None:
        data = {
            "date": ["No data"],
            "quantity": [0]
        }
    else:
        date = sales_data["date"]
        quantity = sales_data["quantity"]
        data = {
            "date": list(date),
            "quantity": list(quantity)
        }
    return JsonResponse(data, safe=False)

def handle_scenario2(request, product_name, period=date.today().year):
    """
    Handles scenario 2 by returning calculated stock levels and orders in JSON format.

    Args:
        request: The HTTP request object.
        product_name: The name of the product.
        period: The year for which to calculate.

    Returns:
        JsonResponse: JSON response containing calculated data.
    """
    sales_data = django_to_df(Sale, request.user,
                              product=product_name, is_product=False)
    product_data = django_to_df(Product, request.user,
                                product=product_name, is_product=True)
    if sales_data is not None:
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        sales_in_year = sales_data[sales_data['date'].dt.year == period]
        sales_in_year = sales_in_year.sort_values(by='date', ascending=True)
        demand = sales_in_year['quantity'].sum()
        date = sales_data["date"]
        unit_cost = product_data.at[0, "unit_cost"]
        fixed_cost = product_data.at[0, "fixed_command_cost"]
        holding_rate = product_data.at[0, "holding_rate"]
        qte_unitaire = product_data.at[0, "qte_unitaire"]
        qty_economic = st.scenario2(
            demand, unit_cost, fixed_cost, holding_rate)
        stock_level = np.zeros(len(sales_in_year))
        order = np.zeros(len(sales_in_year))
        if qte_unitaire - sales_in_year.iloc[0]['quantity'] < 0:
            order[0] = qty_economic * (
                ((sales_in_year.iloc[0]['quantity'] - qte_unitaire)
                // qty_economic)
                + 1
            )
        stock_level[0] = (
            qte_unitaire - sales_in_year.iloc[0]['quantity'] + order[0]
        )
<<<<<<< HEAD
    sales_in_year['stock_level'] = stock_level
    sales_in_year['order'] = order
    date = sales_in_year["date"]
    data = {
        "date": list(date),
        "quantity": list(sales_in_year['quantity']),
        "stock_level": list(sales_in_year['stock_level']),
        "order": list(sales_in_year['order'])
    }
=======
        for i in range(1, len(sales_in_year)):
            if stock_level[i-1] - sales_in_year.iloc[i]['quantity'] < 0:
                order[i] = qty_economic * (
                    ((sales_in_year.iloc[i]['quantity'] - stock_level[i-1]) // qty_economic)
                    + 1
                    )
            stock_level[i] = (
                stock_level[i-1] - sales_in_year.iloc[i]['quantity'] + order[i]
            )
        sales_in_year['stock_level'] = stock_level
        sales_in_year['order'] = order
        date = sales_in_year["date"]
        data = {
            "date": list(date),
            "quantité": list(sales_in_year['quantity']),
            "stock_level": list(sales_in_year['stock_level']),
            "order": list(sales_in_year['order'])
        }
    else:
        data = {
            "date": [0],
            "quantité": ["No data"],
            "stock_level": ["No data"],
            "order":  ["No data"]
        }
>>>>>>> 311c758786f5a48941a672c7a916a16c85c1b217
    return JsonResponse(data, safe=False)

