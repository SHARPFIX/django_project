from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vendor

class VendorSignUpForm(UserCreationForm):
    shop_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'shop_name', 'contact_number', 'address']
