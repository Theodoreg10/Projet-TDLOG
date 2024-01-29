## Forms
module for forms management a Projet-TDLOG/stockmng/principal/forms.py

### dependencies
```python
from django import forms
from .models import Product, Sale
from django.core.exceptions import ValidationError
```
### class
##### LoginForm:
  form responsible for the user login
  <details>
    <summary>See the code</summary>
  Form for user login.
    
  Fields:
  - username (CharField): User's username.
  - password (CharField): User's password (masked).

    ```python
    class LoginForm(forms.Form):
        username = forms.CharField(label="Username")
        password = forms.CharField(widget=forms.PasswordInput, label="Password")
    ```
  </details>
  
##### RegistrationForm
  Form for user registration.

  Fields:
  - name (CharField): User's name.
  - password (CharField): User's password (masked).
  - email (EmailField): User's email address.

<details>
  <summary>
    full code
  </summary>
  
  ```python
  class RegistrationForm(forms.Form):
      name = forms.CharField()
      password = forms.CharField(widget=forms.PasswordInput)
      email = forms.EmailField()
  ```
</details>

##### ProductForm
Form for adding or editing product information.

Fields:
- product_name (CharField): Product name.
- qte_unitaire (IntegerField): Unit quantity.
- unit_cost (DecimalField): Unit cost.
- fixed_command_cost (DecimalField): Fixed command cost.
- holding_rate (DecimalField): Holding rate.
- service_level (DecimalField): Service level.
  
<details>
  <summary>
    full code
  </summary>
  
  ```python
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
  ```
</details>

##### SaleForm
  Form for adding or editing sale information.

  Fields:
  - quantity (IntegerField): Sale quantity.
  - date (DateField): Sale date.
<details>
  <summary>
    full code
  </summary>

  ```python
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
```
</details>

##### function validate_file_extension
Custom validator for file upload forms.

Args:
- value (File): Uploaded file.

Raises:
- ValidationError: If the file extension is not .xlsx or .csv.
<details>
  <summary>
    full code
  </summary>

```python
def validate_file_extension(value):
    if not value.name.endswith(".xlsx") and not value.name.endswith(".csv"):
        raise ValidationError("Only .xlsx and .csv files are allowed.")
```
</details>

##### FileUploadForm
Form for uploading files using the file extension validator.

Fields:
- file (FileField): Uploaded file.
<details>
  <summary>
    full code
  </summary>

  ```python
class FileUploadForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])
```

</details>

##### ProductSelectionForm
Form for product selection.

Fields:
- product (ModelChoiceField): Select a product from available choices.
<details>
  <summary>
    full code
  </summary>

  ```python
class ProductSelectionForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        to_field_name="product_name"
        )
```
</details>

##### ContactForm
Form for contacting support or users.

Fields:
- name (CharField): User's name.
- email (EmailField): User's email address.
- message (CharField): Message to send.
<details>
  <summary>Full code</summary>

  ```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```
</details>

##### ScenarioForm
Form for selecting a scenario.

Fields:
- scenario (ChoiceField): Choose a scenario from predefined options.
<details>
  <summary>full code</summary>

```python
class ScenarioForm(forms.Form):
    SCENARIO_CHOICES = [
        ('scenario1', 'Scenario 1'),
        ('scenario2', 'Scenario 2'),
        ('scenario3', 'Scenario 3'),
        ('scenario4', 'Scenario 4'),
    ]
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, label='Scenario')
```
</details>
