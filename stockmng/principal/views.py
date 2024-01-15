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
import locale
from datetime import date
import numpy as np
import json

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


# Create your views here.


def handle_home_page(request):
    return render(request, "home.html")


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


def handle_about_page(request):
    return render(request, "about.html")


@login_required(login_url="login")
def handle_dashboard_page(request):
    product_selection_form = ProductSelectionForm()
    scenario_form = ScenarioForm()
    context = {
        "product_selection_form": product_selection_form,
        "scenario_form": scenario_form,
    }
    return render(request, "dashboard.html", context)


def handle_login_page(request):
    if request.method == "POST":
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
    else:
        form = LoginForm()
        error_message = None
    context = {"form": form, "error_message": error_message}
    return render(request, "login.html", context)


def handle_logout_view(request):
    logout(request)
    return redirect("login")


def handle_register_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]

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
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
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
    else:
        return JsonResponse({"status": "error"})


@login_required(login_url="login")
def add_sale(request):
    if request.method == "POST":
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
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, sep=";")
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)

            for _, row in df.iterrows():
                Product.objects.create(
                    product_name=row["Product name"],
                    qte_unitaire=row["Qte unitaire"],
                    unit_cost=row["Unit cost"],
                    fixed_command_cost=row["Fixed command cost"],
                    holding_rate=row["Holding rate"],
                    service_level=row["Service level"],
                    user=request.user,
                )
            return redirect("data")
    else:
        form = FileUploadForm()
    return render(request, "data.html", {"form": form})


def handle_file_sales_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, sep=";")
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
            for _, row in df.iterrows():
                product = Product.objects.get(
                    product_name=row["Ref"], user=request.user
                )
                Sale.objects.create(
                    date=row["Date"],
                    quantity=row["Quantity"],
                    ref=product,
                    user=request.user,
                )
            return redirect("data")
    else:
        form = FileUploadForm()
    return render(request, "data.html", {"form": form})


def get_product_details(request, product_name):
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


@login_required(login_url="login")
def handle_contact_page(request):
    if request.method == "POST":
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


def handle_scenario(request, scenario, product_name, period):
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
                                        holding_rate)
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
                                            holding_rate)
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
            print("ok", order_df)
            print("bon", demand)
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
            "command_cost": command_cost,
            "buying_cost": buying_cost,
            "inventory_cost": inventory_cost,
            "total_cost": command_cost + buying_cost + inventory_cost,
            "eoq": eoq
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
            "total_cost": 0,
            "eoq": 0
        }
    return JsonResponse(data, safe=False)


def handle_scenario2(request, product_name, period=date.today().year):
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
        qty_economic = st.scenario2(demand, unit_cost, fixed_cost,
                                    holding_rate)
        stock_level = np.zeros(len(sales_in_year))
        order = np.zeros(len(sales_in_year))
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
                         - stock_level[i - 1])
                        // qty_economic
                    )
                    + 1
                )
            stock_level[i] = (
                stock_level[i - 1]
                - sales_in_year.iloc[i]["quantity"] + order[i]
            )
        sales_in_year["stock_level"] = stock_level
        sales_in_year["order"] = order
        sales_in_year["month"] = sales_in_year["date"].dt.to_period("M")
        sales_data_grouped = (
            sales_in_year.drop("date", axis=1)
            .groupby("month").sum().reset_index()
        )
        sales_data_grouped["month"] = sales_data_grouped["month"].astype(str)
        data = {
            "date": list(sales_data_grouped["month"]),
            "quantité": list(sales_data_grouped["quantity"]),
            "stock_level": list(sales_data_grouped["stock_level"]),
            "order": list(sales_data_grouped["order"]),
            "demand_all_product": list(completes_Sales["quantity"]),
            "product_names": list(completes_Sales["product_name"]),
        }
    else:
        data = {
            "date": [0],
            "quantité": ["No data"],
            "stock_level": ["No data"],
            "order": ["No data"],
            "demand_all_product": list(completes_Sales["quantity"]),
            "product_names": list(completes_Sales["product_name"]),
        }
    return JsonResponse(data, safe=False)
