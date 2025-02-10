from django.contrib import admin
from .models import Seller, Product

class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'approved']
    list_filter = ['approved']
    search_fields = ['user__username', 'store_name']

admin.site.register(Seller, SellerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'available', 'created_at')
    list_filter = ('category', 'available', 'created_at')
    search_fields = ('name', 'description', 'category')

# Register the Product model with custom admin settings
admin.site.register(Product, ProductAdmin)