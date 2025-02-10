from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)  # Requires admin approval
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True)  
    store_description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.store_name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FRUITS', 'Fruits'),
        ('VEGETABLES', 'Vegetables'),
        ('DAIRY', 'Dairy Products'),
        ('MEAT', 'Meat & Poultry'),
        ('GRAINS', 'Grains & Cereals'),
        # ('HERBS', 'Herbs & Spices'),
        # ('BAKERY', 'Bakery & Pastries'),
        # ('BEVERAGES', 'Beverages'),
        # ('ORGANIC', 'Organic Products'),
        # ('NUTS', 'Nuts & Seeds'),
        # ('OILS', 'Oils & Vinegars'),
        # ('JAMS', 'Jams & Preserves'),
        # ('HONEY', 'Honey & Sweeteners'),
        # ('DRIED', 'Dried Fruits'),
        # ('FROZEN', 'Frozen Foods'),
        # ('EGGS', 'Eggs'),
        # ('CONDIMENTS', 'Condiments & Sauces'),
        # ('SNACKS', 'Snacks & Confections'),
        # ('TEA', 'Tea & Coffee'),
        # ('HEALTH', 'Health & Wellness'),
        # ('FLOWERS', 'Flowers & Plants'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='FRUITS')

    def __str__(self):
        return self.name