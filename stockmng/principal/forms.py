from django import forms
from .models import Product, Sale
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class RegistrationForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class ProductForm(forms.ModelForm):
    product_name = forms.CharField(label="Product Name")
    qte_unitaire = forms.IntegerField(label="Unit Quantity")
    unit_cost = forms.DecimalField(label="Unit Cost")
    fixed_command_cost = forms.DecimalField(label="Fixed Command Cost")
    holding_rate = forms.DecimalField(label="Holding Rate")
    service_level = forms.DecimalField(label="Service Level")

    class Meta:
        model = Product
        fields = [
            "product_name",
            "qte_unitaire",
            "unit_cost",
            "fixed_command_cost",
            "holding_rate",
            "service_level",
        ]


class SaleForm(forms.ModelForm):
    quantity = forms.IntegerField(label="Quantity")
    date = forms.DateField(
        label="Sale Date", widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Sale
        fields = ["ref", "quantity", "date"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(SaleForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["ref"].queryset = Product.objects.filter(user=user)


def validate_file_extension(value):
    if not value.name.endswith(".xlsx") and not value.name.endswith(".csv"):
        raise ValidationError("Only .xlsx and .csv files are allowed.")


class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])


class ProductSelectionForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        to_field_name="product_name"
        )


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class ScenarioForm(forms.Form):
    SCENARIO_CHOICES = [
        ('scenario1', 'Scenario 1'),
        ('scenario2', 'Scenario 2'),
        ('scenario3', 'Scenario 3'),
    ]
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, label='Scenario')
