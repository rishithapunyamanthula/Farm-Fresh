from django.db import models
from django.contrib.auth.models import User
from sellers.models import Product

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.state}, {self.country}"

class PaymentInformation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5)  # Format: MM/YY
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"**** **** **** {self.card_number[-4:]}"


class SubscriptionBox(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boxes')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    is_active = models.BooleanField(default=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='subscription_boxes')
    payment_method = models.ForeignKey('PaymentInformation', on_delete=models.CASCADE, related_name='subscription_boxes')

    def __str__(self):
        return self.name

class BoxProduct(models.Model):
    box = models.ForeignKey(SubscriptionBox, on_delete=models.CASCADE, related_name='box_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.box.name}"
    
# Comment and Rating model
class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=1)  # Rating scale: 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.customer.user.username} on {self.product.name}'

# Product question model
class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField(blank=True, null=True)  # Seller's response
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Question by {self.customer.user.username} on {self.product.name}'