from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.seller_register, name='seller_register'),
    path('login/', views.seller_login, name='seller_login'),
    path('home/', views.seller_home, name='seller_home'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('availability_product/<int:product_id>/', views.availability_product, name='availability_product'),
    path('quantity_product/<int:product_id>/', views.quantity_product, name='quantity_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('inventory/', views.view_inventory, name='view_inventory'),
    path('update_profile/', views.update_seller_profile, name='update_seller_profile'),
    path('comments-ratings/', views.view_comments_ratings, name='view_comments_ratings'),
    path('questions/', views.view_and_answer_questions, name='view_and_answer_questions'),
    path('questions/<int:question_id>/respond/', views.respond_to_question, name='respond_to_question'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('statistics/', views.seller_statistics, name='seller_statistics'),
]
