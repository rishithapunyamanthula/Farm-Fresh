from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SellerSignupForm, LoginForm, ProductForm, SellerProfileUpdateForm, ProductEdit, ProductQuantity, ProductAvailability
from .models import Seller, Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from customers.models import ProductComment, ProductQuestion, BoxProduct
from customers.forms import ProductQuestionResponseForm
from django.utils import timezone
from django.db.models import Avg, Count



def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

@login_required(login_url='seller_login')
def seller_dashboard(request):
    return render(request, 'sellers/dashboard.html')

def seller_register(request):
    clear_messages(request)
    if request.method == 'POST':
        form = SellerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('seller_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SellerSignupForm()
    return render(request, 'sellers/seller_register.html', {'form': form})

def seller_login(request):
    clear_messages(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    seller = Seller.objects.get(user=user)
                    if seller.approved:
                        login(request, user)
                        messages.success(request, 'Login successful!')
                        return redirect('seller_home')
                    else:
                        messages.error(request, 'Your account is not approved by the admin yet.')
                except Seller.DoesNotExist:
                    messages.error(request, 'You are not registered as a seller.')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'sellers/seller_login.html', {'form': form})

def seller_home(request):
    clear_messages(request)
    return render(request, 'sellers/seller_home.html')


# Add New Product
@login_required(login_url='seller_login')
def add_product(request):
    clear_messages(request)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('view_inventory')
    else:
        form = ProductForm()
    return render(request, 'sellers/add_product.html', {'form': form})

# Edit Product
@login_required(login_url='seller_login')
def edit_product(request, product_id):
    clear_messages(request)
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductEdit(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_inventory')
    else:
        form = ProductEdit(instance=product)
    return render(request, 'sellers/edit_product.html', {'form': form})

@login_required(login_url='seller_login')
def availability_product(request, product_id):
    clear_messages(request)
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductAvailability(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_inventory')
    else:
        form = ProductAvailability(instance=product)
        print(form)
    return render(request, 'sellers/availability_product.html', {'form': form})

@login_required(login_url='seller_login')
def quantity_product(request, product_id):
    clear_messages(request)
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductQuantity(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_inventory')
    else:
        form = ProductQuantity(instance=product)
    return render(request, 'sellers/quantity_product.html', {'form': form})

# Delete Product
@login_required(login_url='seller_login')
def delete_product(request, product_id):
    clear_messages(request)
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('view_inventory')
    return render(request, 'sellers/delete_product.html', {'product': product})

# View Product Inventory
@login_required(login_url='seller_login')
def view_inventory(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    paginator = Paginator(products, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sellers/view_inventory.html', {'page_obj': page_obj})


@login_required(login_url='seller_login')
def update_seller_profile(request):
    seller = Seller.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = SellerProfileUpdateForm(request.POST, instance=seller)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('update_seller_profile')
    else:
        form = SellerProfileUpdateForm(instance=seller)
    
    return render(request, 'sellers/update_profile.html', {'form': form})


# View comments and ratings for products
@login_required(login_url='seller_login')
def view_comments_ratings(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'sellers/view_comments_ratings.html', {'products': products})

# View questions and answer them
@login_required(login_url='seller_login')
def view_and_answer_questions(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'sellers/view_questions.html', {'products': products})

# Respond to a product question
@login_required(login_url='seller_login')
def respond_to_question(request, question_id):
    question = get_object_or_404(ProductQuestion, id=question_id, product__seller=request.user)
    if request.method == 'POST':
        form = ProductQuestionResponseForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.answered_at = timezone.now()
            question.save()
            messages.success(request, 'Question answered successfully!')
            return redirect('view_and_answer_questions')
    else:
        form = ProductQuestionResponseForm(instance=question)
    return render(request, 'sellers/respond_to_question.html', {'form': form, 'question': question})


@login_required(login_url='seller_login')
def seller_statistics(request):
    # Get the seller's products
    products = Product.objects.filter(seller=request.user)

    # Data for the charts
    avg_rating_data_points = []
    subscription_count_data_points = []

    for product in products:
        # Average rating for each product
        avg_rating = product.comments.aggregate(average_rating=Avg('rating'))['average_rating'] or 0
        # Subscription count for each product
        subscription_count = BoxProduct.objects.filter(product=product).count()

        # Add to data points
        avg_rating_data_points.append({"label": product.name, "y": avg_rating})
        subscription_count_data_points.append({"label": product.name, "y": subscription_count})
    print(avg_rating_data_points)
    context = {
        "avg_rating_data_points": avg_rating_data_points,
        "subscription_count_data_points": subscription_count_data_points,
    }

    return render(request, 'sellers/seller_statistics.html', context)