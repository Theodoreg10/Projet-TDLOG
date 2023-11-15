from django import forms
from .models import Product, Sale


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class RegistrationForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class ProductForm(forms.ModelForm):
    product_name = forms.CharField(label='Product Name')
    qte_unitaire = forms.IntegerField(label='Unit Quantity')
    unit_cost = forms.DecimalField(label='Unit Cost')
    fixed_command_cost = forms.DecimalField(label='Fixed Command Cost')
    holding_rate = forms.DecimalField(label='Holding Rate')
    service_level = forms.DecimalField(label='Service Level')

    class Meta:
        model = Product
        fields = [
            'product_name',
            'qte_unitaire',
            'unit_cost',
            'fixed_command_cost',
            'holding_rate',
            'service_level']


class SaleForm(forms.ModelForm):
    quantity = forms.IntegerField(label='Quantity')
    date = forms.DateField(
        label='Sale Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Sale
        fields = ['ref', 'quantity', 'date']
