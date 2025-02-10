from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.customer_register, name='customer_register'),
    path('login/', views.customer_login, name='customer_login'),
    path('home/', views.customer_home, name='customer_home'),
    path('view_profile/', views.view_customer_profile, name='view_customer_profile'),
    path('add_address/', views.add_address, name='add_address'),
    path('add_payment/', views.add_payment_information, name='add_payment_information'),
    path('update_profile/', views.update_customer_profile, name='update_customer_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products_by_category/', views.browse_products_by_category, name='browse_products_by_category'),
    path('create-box/', views.create_subscription_box, name='create_subscription_box'),
    path('product/<int:product_id>/add-to-box/', views.add_product_to_box, name='add_product_to_box'),
    path('subscriptions/', views.view_subscriptions, name='view_subscriptions'),
    path('subscriptions/<int:box_id>/toggle/', views.toggle_subscription_status, name='toggle_subscription_status'),
    path('subscriptions/<int:box_id>/delete-product/<int:product_id>/', views.delete_product_from_box, name='delete_product_from_box'),
    path('product/<int:product_id>/add-comment/', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/add-question/', views.add_question, name='add_question'),
]
