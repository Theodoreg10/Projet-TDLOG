# Generated by Django 4.2.7 on 2023-11-15 19:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("principal", "0003_alter_product_fixed_command_cost_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="unit_cost",
            field=models.FloatField(),
        ),
    ]
