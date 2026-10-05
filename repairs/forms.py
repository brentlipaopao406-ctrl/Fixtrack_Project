from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Technician


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "autocomplete": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "autocomplete": "current-password"}))


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ["name", "specialization", "phone", "email", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Juan Dela Cruz"}),
            "specialization": forms.TextInput(attrs={"placeholder": "e.g. Computer & Network Technician"}),
            "phone": forms.TextInput(attrs={"placeholder": "09xxxxxxxxx"}),
            "email": forms.EmailInput(attrs={"placeholder": "technician@example.com"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Category name"}),
            "description": forms.TextInput(attrs={"placeholder": "Short description"}),
        }
