from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class RegistrationForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()