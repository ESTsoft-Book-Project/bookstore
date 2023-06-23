from django import forms
from .models import Product, Comment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'stock']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']