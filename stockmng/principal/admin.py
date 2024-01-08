from django.contrib import admin

# Register your models here.
from .models import Product, Sale


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "qte_unitaire", "user")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("date", "quantity", "ref", "user")
