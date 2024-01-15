from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Represents a product in the system.

    Fields:
    - product_name (CharField): The name of the product.
    - qte_unitaire (IntegerField): The unit quantity of the product.
    - unit_cost (FloatField): The unit cost of the product.
    - fixed_command_cost (FloatField): The fixed command cost of the product.
    - holding_rate (FloatField): The holding rate of the product.
    - service_level (FloatField): The service level of the product.
    - user (ForeignKey to User): The user who owns the product.

    Methods:
    - __str__(): Returns a string representation of the product.

    """
    product_name = models.CharField(max_length=255)
    qte_unitaire = models.IntegerField()
    unit_cost = models.FloatField()
    fixed_command_cost = models.FloatField()
    holding_rate = models.FloatField()
    service_level = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Sale(models.Model):
    """
    Represents a sale transaction in the system.

    Fields:
    - date (DateField): The date of the sale.
    - quantity (IntegerField): The quantity sold.
    - ref (ForeignKey to Product): The product sold in the sale.
    - user (ForeignKey to User): The user who made the sale.

    Methods:
    - __str__(): Returns a string representation of the sale.

    """
    date = models.DateField()
    quantity = models.IntegerField()
    ref = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.ref.product_name} on {self.date}"
