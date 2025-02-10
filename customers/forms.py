from django import forms
from django.contrib.auth.models import User
from .models import Customer,Address, PaymentInformation, SubscriptionBox, Address, PaymentInformation, BoxProduct, ProductComment, ProductQuestion

# Customer Signup Form
class CustomerSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }

    phone_number = forms.CharField(max_length=15, required=True)

# Profile Update Form
class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number']

# Address Form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'city', 'state', 'postal_code', 'country']

# Payment Information Form
class PaymentInformationForm(forms.ModelForm):
    class Meta:
        model = PaymentInformation
        fields = ['card_number', 'cardholder_name', 'expiry_date', 'cvv']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SubscriptionBoxForm(forms.ModelForm):
    address = forms.ModelChoiceField(queryset=None, empty_label="Select an address")
    payment_method = forms.ModelChoiceField(queryset=None, empty_label="Select a payment method")

    class Meta:
        model = SubscriptionBox
        fields = ['name', 'description', 'frequency', 'is_active', 'address', 'payment_method']

    def __init__(self, user, *args, **kwargs):
        super(SubscriptionBoxForm, self).__init__(*args, **kwargs)
        # Filter addresses and payment methods for the current user
        self.fields['address'].queryset = Address.objects.filter(customer=user.customer)
        self.fields['payment_method'].queryset = PaymentInformation.objects.filter(customer=user.customer)

# Form to add a product to a box
class AddProductToBoxForm(forms.Form):
    box = forms.ModelChoiceField(queryset=None, empty_label="Select a box")

    def __init__(self, user, *args, **kwargs):
        super(AddProductToBoxForm, self).__init__(*args, **kwargs)
        self.fields['box'].queryset = SubscriptionBox.objects.filter(customer=user)

# Form for adding comments and ratings
class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])  # Rating scale from 1 to 5
        }

# Form for asking a question about the product
class ProductQuestionForm(forms.ModelForm):
    class Meta:
        model = ProductQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3})
        }

# Form for the seller to respond to a question
class ProductQuestionResponseForm(forms.ModelForm):
    class Meta:
        model = ProductQuestion
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 3})
        }