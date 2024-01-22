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
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import pandas as pd
from stock_package import django_to_df
import stock_package as st
import locale
from datetime import date
import numpy as np
import json
from pulp import (
    LpVariable, LpProblem, LpMinimize, LpBinary, lpSum, value, PULP_CBC_CMD
)
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


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


@login_required(login_url="login")
def handle_data_page(request):
    """
    Renders the data page for logged in users.
    Shows products and sales related to the user.

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
    context = {
        "products": products,
        "sales": sales,
        "form_product": form_product,
        "form_sale": form_sale,
        "file_upload_form": file_upload_form,
    }
    return render(request, "data.html", context)


def handle_about_page(request):
    return render(request, "about.html")


@login_required(login_url="login")
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
        "product_selection_form": product_selection_form,
        "scenario_form": scenario_form,
    }
    return render(request, "dashboard.html", context)


def handle_login_page(request):
    """View function for the login page and handling login actions. Args:
    Request: Http Request.
    Returns:
    Rendered login page."""
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


def handle_logout_view(request):
    """
    Logs the user out and redirects to the login page.

    Args:
        Request: Http Request.

    Returns:
        Redirected login page.
    """

    logout(request)
    return redirect("login")


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


@login_required(login_url="login")
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
            try:
                product.save()
            except IntegrityError:
                messages.error(request, 'Product already exists')
                sale_form = SaleForm(user=request.user)
                product_form = ProductForm()
                context = {"form_sale": sale_form,
                           "form_product": product_form}
                return render(request, "data.html", context)
            return redirect("data")
    else:
        sale_form = SaleForm(user=request.user)
        product_form = ProductForm()
        context = {"form_sale": sale_form, "form_product": product_form}
    return render(request, "data.html", context)


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


@login_required(login_url="login")
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
            return redirect("data")
    else:
        sale_form = SaleForm(user=request.user)
        product_form = ProductForm()
        context = {"form_sale": sale_form, "form_product": product_form}
    return render(request, "data.html", context)


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
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, sep=";")
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)

            for _, row in df.iterrows():
                try:
                    Product.objects.create(
                        product_name=row["Product name"],
                        qte_unitaire=row["Qte unitaire"],
                        unit_cost=row["Unit cost"],
                        fixed_command_cost=row["Fixed command cost"],
                        holding_rate=row["Holding rate"],
                        service_level=row["Service level"],
                        user=request.user,
                    )
                except IntegrityError:
                    messages.error(
                        request,
                        f'Error creating product {row["Product name"]}.'
                        )
                    continue
            return redirect("data")
    else:
        form = FileUploadForm()
    return render(request, "data.html", {"form": form})


@login_required(login_url='login')
def handle_file_sales_upload(request):
    """
    Handles the download of sales data from a file uploaded by the user,
    and updates the database.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'data' page upon successful upload.
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, sep=";")
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
            for _, row in df.iterrows():
                try:
                    product = Product.objects.get(
                        product_name=row["Ref"], user=request.user
                    )
                    Sale.objects.create(
                        date=row["Date"],
                        quantity=row["Quantity"],
                        ref=product,
                        user=request.user,
                    )
                except ObjectDoesNotExist:
                    messages.error(request,
                                   f'Product {row["Ref"]} does not exist.')
                    continue
                except Exception:
                    messages.error(
                        request,
                        f'Error creating sale for product {row["Ref"]}')
                    continue
            return redirect("data")
    else:
        form = FileUploadForm()
    return render(request, "data.html", {"form": form})


def get_product_details(request, product_name):
    """
    Returns product details in JSON format.

    Args:
        request: The HTTP request object.
        product_name: The name of the product.

    Returns:
        JsonResponse: JSON response containing product details.
    """
    product = Product.objects.get(product_name=product_name, user=request.user)
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


@login_required(login_url='login')
def handle_contact_page(request):
    """
    Handles the submission of the contact form and sends an email.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'contact' page
        upon successful form submission.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name", "")
            last_name = form.cleaned_data.get("last_name", "")

            message = (f"From: {name} {last_name}\n\n"
                       f"{form.cleaned_data['message']}")
            send_mail(
                "Contact Form Submission",  # subject
                message,  # message
                form.cleaned_data["email"],  # from email
                ["theodoregnimavo6@gmail.com"],  # to email
            )
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"contact_form": form})


def handle_scenario(request, scenario, product_name, period=date.today().year):
    """
    Handles a scenario by querying product and sales data,
    and displaying DataFrames.

    Args:
        request: The HTTP request object.
    """
    sales_data = django_to_df(
        Sale, request.user, product=product_name, is_product=False
    )
    product_data = django_to_df(
        Product, request.user, product=product_name, is_product=True
    )
    completes_Sales = django_to_df(Sale, request.user, is_product=False)
    completes_products = django_to_df(
        Product, request.user, is_product=True)
    completes_Sales = completes_Sales.merge(
        completes_products[["id", "product_name"]],
        left_on="ref_id",
        right_on="id",
        how="left",
    )
    completes_Sales["date"] = pd.to_datetime(completes_Sales["date"])
    completes_Sales = (completes_Sales[completes_Sales["date"]
                                       .dt.year == period])
    completes_Sales = (
        completes_Sales[["product_name", "quantity"]]
        .groupby("product_name")
        .sum()
        .reset_index()
    )
    if sales_data is not None:
        sales_data["date"] = pd.to_datetime(sales_data["date"])
        sales_in_year = sales_data[sales_data["date"].dt.year == period]
        sales_in_year = sales_in_year.sort_values(by="date", ascending=True)
        demand = sales_in_year["quantity"].sum()
        unit_cost = product_data.at[0, "unit_cost"]
        fixed_cost = product_data.at[0, "fixed_command_cost"]
        holding_rate = product_data.at[0, "holding_rate"]
        qte_unitaire = product_data.at[0, "qte_unitaire"]
        stock_level = np.zeros(len(sales_in_year))
        order = np.zeros(len(sales_in_year))
        if scenario == "scenario1":
            order = list(sales_in_year['quantity'])
            order[0] = order[0] - qte_unitaire
            stock_level[0] = (qte_unitaire + order[0]
                              - sales_in_year.iloc[0]["quantity"])
            for i in range(1, len(sales_in_year)):
                stock_level[i] = (stock_level[i - 1]
                                  + order[i]
                                  - sales_in_year.iloc[i]["quantity"])
            eoq = 0
        elif scenario == "scenario2":
            qty_economic = st.scenario2(demand, unit_cost, fixed_cost,
                                        holding_rate/100)
            eoq = qty_economic
            if qte_unitaire - sales_in_year.iloc[0]["quantity"] < 0:
                order[0] = qty_economic * (
                    ((sales_in_year.iloc[0]["quantity"]
                      - qte_unitaire) // qty_economic)
                    + 1
                )
            stock_level[0] = (
                qte_unitaire - sales_in_year.iloc[0]["quantity"] + order[0]
            )
            for i in range(1, len(sales_in_year)):
                if stock_level[i - 1] - sales_in_year.iloc[i]["quantity"] < 0:
                    order[i] = qty_economic * (
                        (
                            (sales_in_year.iloc[i]["quantity"]
                             - stock_level[i - 1]) // qty_economic
                        )
                        + 1
                    )
                stock_level[i] = (
                    stock_level[i - 1]
                    - sales_in_year.iloc[i]["quantity"] + order[i]
                )
        elif scenario == "scenario3":
            if demand > qte_unitaire:
                qty_economic = st.scenario2(demand - qte_unitaire,
                                            unit_cost,
                                            fixed_cost,
                                            holding_rate/100)
                eoq = qty_economic
                nbr_command = demand / eoq
                frequency = 1 / nbr_command
                periodicity = 365 * frequency
            else:
                qty_economic = 0
                eoq = qty_economic
                nbr_command = 0
                frequency = 0
                periodicity = 0
            order_df = pd.DataFrame(columns=['Date', 'Order'])
            dates_annuelle = pd.date_range(start=f'{period}-01-01',
                                           end=f'{period}-12-31')
            print("bon", frequency)
            for i, date2 in enumerate(dates_annuelle):
                if int(periodicity) != 0:
                    periodicity = int(periodicity)
                    if i % periodicity == 0:
                        order_df = pd.concat([order_df,
                                              pd.DataFrame({'Date': [date2],
                                                            'Order': [eoq]})],
                                             ignore_index=True)
                    else:
                        order_df = pd.concat([order_df,
                                              pd.DataFrame({'Date': [date2],
                                                            'Order': [0]})],
                                             ignore_index=True)
                else:
                    nb = int(nbr_command/len(dates_annuelle))+1
                    count = 0
                    if count*nb < nbr_command:
                        order_df = pd.concat(
                            [order_df,
                             pd.DataFrame({'Date': [date2],
                                           'Order': [nb*eoq]})],
                            ignore_index=True)
                        count += 1
                    else:
                        order_df = pd.concat([order_df,
                                              pd.DataFrame({'Date': [date2],
                                                            'Order': [0]})],
                                             ignore_index=True)
            order_df['Date'] = pd.to_datetime(order_df['Date'])
            order_df = order_df.groupby('Date').sum().reset_index()
            order_df = order_df.merge(sales_in_year, left_on='Date',
                                      right_on='date', how='left')
            order_df = order_df[['Date', 'Order', 'quantity']]
            order_df = order_df.fillna(0)
            order = list(order_df['Order'])
            order_df['date'] = order_df['Date']
            sales_in_year = order_df.drop('Order', axis=1)
            sales_in_year = sales_in_year.sort_values(by="date",
                                                      ascending=True)
            sales_in_year = sales_in_year.drop('Date', axis=1)
            order = list(order_df['Order'])
            stock_level = np.zeros(len(sales_in_year))
            stock_level[0] = (
                qte_unitaire - sales_in_year.iloc[0]["quantity"] + order[0]
            )
            for i in range(1, len(sales_in_year)):
                stock_level[i] = (
                    stock_level[i - 1]
                    - sales_in_year.iloc[i]["quantity"] + order[i]
                )
        elif scenario == "scenario4":
            date_range = pd.date_range(start=f'{period}-01-01',
                                       end=f'{period}-12-31')
            data_sales = pd.DataFrame(columns=['Date'])
            data_sales['Date'] = date_range
            data_sales = data_sales.merge(sales_in_year, left_on='Date',
                                          right_on='date', how='left')
            data_sales['date'] = data_sales['Date']
            data_sales = data_sales.fillna(0)
            data_sales = data_sales[['date', 'quantity']]
            n = len(data_sales)
            demande_journaliere = list(data_sales['quantity'])
            x = LpVariable.dicts("Quantite_commandee", range(n), lowBound=0)
            s = LpVariable.dicts("Stock", range(n), lowBound=0)
            probleme = LpProblem("Probleme_EOQ", LpMinimize)
            z = LpVariable.dicts("z", range(n), cat=LpBinary)
            probleme += (
                (holding_rate/100)*unit_cost*lpSum(s[j] for j in range(n)) / n
                + fixed_cost*lpSum(z[j] for j in range(n))
                + unit_cost*lpSum(x[j] for j in range(n)), "Moyenne_x")
            for j in range(n):
                probleme += x[j] >= 0
                probleme += x[j] <= z[j] * demand
                probleme += s[j] >= 0
            probleme += s[0] == x[0] + qte_unitaire - demande_journaliere[0]
            for j in range(1, n):
                probleme += s[j] == s[j-1] + x[j] - demande_journaliere[j]
            probleme.solve(PULP_CBC_CMD(msg=1, timeLimit=20))
            sales_in_year = pd.DataFrame(columns=['date'])
            sales_in_year['date'] = data_sales['date']
            sales_in_year['date'] = pd.to_datetime(sales_in_year['date'])
            sales_in_year['quantity'] = demande_journaliere
            order = ([value(x[var]) for var in x])
            stock_level = np.zeros(n)
            stock_level[0] = (
                qte_unitaire - sales_in_year.iloc[0]["quantity"] + order[0]
            )
            for i in range(1, len(sales_in_year)):
                stock_level[i] = (
                    stock_level[i - 1]
                    - sales_in_year.iloc[i]["quantity"] + order[i]
                )
            eoq = 0
        sales_in_year["stock_level"] = stock_level
        sales_in_year["order"] = order
        sales_in_year["month"] = sales_in_year["date"].dt.to_period("M")
        inventory_data = (sales_in_year[['date', 'stock_level']]
                          .groupby('date').sum())
        date_range = pd.date_range(start=inventory_data.index.min(),
                                   end=inventory_data.index.max(), freq='D')
        inventory_data = inventory_data.reindex(date_range)
        inventory_level = list(inventory_data['stock_level'])
        if pd.isna(inventory_level[0]):
            inventory_level[0] = 0
        for i in range(1, len(inventory_data)):
            if pd.isna(inventory_level[i]):
                inventory_level[i] = inventory_level[i - 1]
        inventory_data = inventory_data.reset_index()
        inventory_data['stock_level'] = inventory_level
        inventory_data['date'] = inventory_data['index']
        inventory_data['month'] = inventory_data['date'].dt.to_period('M')
        inventory_data = inventory_data.groupby('month').mean().reset_index()
        sales_data_grouped = (
            sales_in_year.drop("date", axis=1)
            .groupby("month").sum().reset_index()
        )
        sales_data_grouped["month"] = sales_data_grouped["month"].astype(str)
        command_cost = 0
        buying_cost = 0
        for order in list(sales_in_year['order']):
            if order > 0:
                command_cost += fixed_cost
                buying_cost += (order * unit_cost)
        inventory_cost = (inventory_data['stock_level'].mean()
                          * holding_rate * unit_cost/100)
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
    else:
        data = {
            "date": [0],
            "quantité": ["No data"],
            "stock_level": ["No data"],
            "order": ["No data"],
            "demand_all_product": list(completes_Sales["quantity"]),
            "product_names": list(completes_Sales["product_name"]),
            "command_cost": 0,
            "buying_cost": 0,
            "inventory_cost": 0,
            "without_budget": 0,
            "total_cost": 0,
            "eoq": 0
        }
    return JsonResponse(data, safe=False)
