from django import forms
from django.core.validators import MinLengthValidator
from django.urls import reverse
import uuid
import os
from .models import Product
from categories.models import Category

# ProductForm class
class ProductForm(forms.ModelForm):
    # meta class
    class Meta:
        # model
        model = Product
        # fields
        fields = ['category', 'name', 'price', 'description', 'image', 'in_stock', 'stock_quantity']
        # widgets
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': '0'}),
        }
        # labels
        labels = {
            'name': 'Product Name',
            'price': 'Price',
            'description': 'Description',
            'image': 'Product Image',
            'in_stock': 'In Stock',
            'stock_quantity': 'Stock Quantity',
        }
        # help_texts
        help_texts = {
            'name': 'Enter the name of the product (minimum 3 characters)',
            'price': 'Enter the price of the product (e.g., 19.99)',
            'description': 'Enter a detailed description of the product',
            'image': 'Upload a clear image of the product (JPG, PNG, GIF)',
            'in_stock': 'Check if the product is currently available',
            'stock_quantity': 'Enter the number of items available in stock',
        }
        # error_messages
        error_messages = {
            'name': {
                'required': 'Product name is required',
                'max_length': 'Product name cannot exceed 200 characters',
            },
            'price': {
                'required': 'Price is required',
                'invalid': 'Please enter a valid price',
            },
            'description': {
                'required': 'Product description is required',
            },
        }
    
    def clean_name(self):
        """Custom validation for product name"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            raise forms.ValidationError('Product name must be at least 3 characters long.')
        return name
    
    def clean_price(self):
        """Custom validation for product price"""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price
    
    def clean_stock_quantity(self):
        """Custom validation for stock quantity"""
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity is not None and stock_quantity < 0:
            raise forms.ValidationError('Stock quantity cannot be negative.')
        return stock_quantity
    
    def clean_image(self):
        """Custom validation for image upload"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (limit to 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be less than 5MB.')

            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError('Please upload a valid image file (JPG, PNG, GIF).')

        return image
