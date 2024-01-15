from django import forms
from .models import Product, Sale
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """
    Form for user login.

    Fields:
    - username (CharField): User's username.
    - password (CharField): User's password (masked).

    """
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class RegistrationForm(forms.Form):
    """
    Form for user registration.

    Fields:
    - name (CharField): User's name.
    - password (CharField): User's password (masked).
    - email (EmailField): User's email address.

    """
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class ProductForm(forms.ModelForm):
    """
    Form for adding or editing product information.

    Fields:
    - product_name (CharField): Product name.
    - qte_unitaire (IntegerField): Unit quantity.
    - unit_cost (DecimalField): Unit cost.
    - fixed_command_cost (DecimalField): Fixed command cost.
    - holding_rate (DecimalField): Holding rate.
    - service_level (DecimalField): Service level.

    """

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
    """
    Form for adding or editing sale information.

    Fields:
    - quantity (IntegerField): Sale quantity.
    - date (DateField): Sale date.

    """
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
    """
    Custom validator for file upload forms.

    Args:
    - value (File): Uploaded file.

    Raises:
    - ValidationError: If the file extension is not .xlsx or .csv.

    """
    if not value.name.endswith(".xlsx") and not value.name.endswith(".csv"):
        raise ValidationError("Only .xlsx and .csv files are allowed.")


class FileUploadForm(forms.Form):
    """
    Form for uploading files.

    Fields:
    - file (FileField): Uploaded file.

    """
    file = forms.FileField(validators=[validate_file_extension])


class ProductSelectionForm(forms.Form):
    """
    Form for product selection.

    Fields:
    - product (ModelChoiceField): Select a product from available choices.

    """
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        to_field_name="product_name"
        )


class ContactForm(forms.Form):
    """
    Form for contacting support or users.

    Fields:
    - name (CharField): User's name.
    - email (EmailField): User's email address.
    - message (CharField): Message to send.

    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class ScenarioForm(forms.Form):
    """
    Form for selecting a scenario.

    Fields:
    - scenario (ChoiceField): Choose a scenario from predefined options.

    """
    SCENARIO_CHOICES = [
        ('scenario1', 'Scenario 1'),
        ('scenario2', 'Scenario 2'),
        ('scenario3', 'Scenario 3'),
    ]
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, label='Scenario')
