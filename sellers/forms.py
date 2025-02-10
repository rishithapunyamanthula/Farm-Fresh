from django import forms
from django.contrib.auth.models import User
from .models import Seller, Product

class SellerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Seller
        fields = ['store_name', 'phone_number', 'address', 'store_description']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        seller = super().save(commit=False)
        seller.user = user
        if commit:
            seller.save()
        return seller

class SellerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['store_name', 'phone_number', 'address', 'store_description']  # Fields to update

    def __init__(self, *args, **kwargs):
        super(SellerProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity','category', 'available', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),  # Optional: Add styling
        }

class ProductEdit(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),  # Optional: Add styling
        }

class ProductAvailability(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),  # Optional: Add styling
        }

class ProductQuantity(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),  # Optional: Add styling
        }
