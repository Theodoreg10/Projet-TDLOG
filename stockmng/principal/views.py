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
import pandas as pd
from stock_package import django_to_df
# Create your views here.


def handle_home_page(request):
    return render(request, "home.html")


@login_required(login_url='login')
def handle_data_page(request):
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
    product_selection_form = ProductSelectionForm()
    scenario_form = ScenarioForm()
    context = {
        'product_selection_form': product_selection_form,
        'scenario_form': scenario_form
    }
    return render(request, "dashboard.html", context)


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


@login_required(login_url='login')
def add_product(request):
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


@login_required(login_url='login')
def add_sale(request):
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
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
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


def handle_file_sales_upload(request):
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
                product = Product.objects.get(product_name=row['Ref'])
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
    product = Product.objects.get(product_name=product_name)
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
    products_query = Product.objects.all()
    sales_query = Sale.objects.all()  
    products_dataframe = django_to_df(products_query)
    sales_dataframe = django_to_df(sales_query)

    # Affichez les DataFrames
    print("Products DataFrame:")
    print(products_dataframe)

    print("\nSales DataFrame:")
    print(sales_dataframe)
