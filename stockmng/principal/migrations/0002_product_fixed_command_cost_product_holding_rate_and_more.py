# Generated by Django 4.2.7 on 2023-11-13 14:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("principal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="fixed_command_cost",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="product",
            name="holding_rate",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="product",
            name="service_level",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="product",
            name="unit_cost",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]