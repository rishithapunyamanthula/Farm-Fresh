from django.contrib import admin
from .models import Customer, Address, PaymentInformation, SubscriptionBox, BoxProduct

# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

# Register Address model
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_line', 'city', 'state', 'country')
    search_fields = ('customer__user__username', 'address_line', 'city', 'state', 'country')

# Register PaymentInformation model
@admin.register(PaymentInformation)
class PaymentInformationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cardholder_name', 'card_number', 'expiry_date')
    search_fields = ('customer__user__username', 'cardholder_name', 'card_number')

# Register SubscriptionBox model
@admin.register(SubscriptionBox)
class SubscriptionBoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'frequency', 'is_active', 'address', 'payment_method')
    search_fields = ('name', 'customer__username', 'frequency')

# Register BoxProduct model
@admin.register(BoxProduct)
class BoxProductAdmin(admin.ModelAdmin):
    list_display = ('box', 'product')
    search_fields = ('box__name', 'product__name')
