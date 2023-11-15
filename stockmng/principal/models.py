from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Product(models.Model):
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
    date = models.DateField()
    quantity = models.IntegerField()
    ref = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.ref.product_name} on {self.date}"
