from django import forms
from .models import Category, Products
class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields='__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'