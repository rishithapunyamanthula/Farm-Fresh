from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Customer, Address, PaymentInformation, SubscriptionBox, BoxProduct, ProductComment, ProductQuestion
from .forms import CustomerSignupForm, CustomerProfileUpdateForm, AddressForm, PaymentInformationForm, LoginForm, SubscriptionBoxForm, AddProductToBoxForm, ProductCommentForm, ProductQuestionForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from sellers.models import Product


def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

def customer_register(request):
    clear_messages(request)
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Create a corresponding Customer object
            phone_number = form.cleaned_data['phone_number']
            Customer.objects.create(user=user, phone_number=phone_number)

            messages.success(request, 'Registration successful!')
            return redirect('customer_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerSignupForm()
    return render(request, 'customers/customer_register.html', {'form': form})

def customer_login(request):
    clear_messages(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                try:
                    customer = Customer.objects.get(user=user)
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('customer_home')
                except Customer.DoesNotExist:
                    messages.error(request, 'You are not registered as a customer.')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'customers/customer_login.html', {'form': form})


@login_required(login_url='customer_login')
def customer_home(request):
    clear_messages(request)
    
    # Get all categories for the dropdown
    categories = Product.CATEGORY_CHOICES

    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')
    availability = request.GET.get('availability', '')

    # Fetch products based on search and filters
    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if selected_category:
        products = products.filter(category=selected_category)

    if availability == 'available':
        products = products.filter(available=True)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'availability': availability,
    }
    return render(request, 'customers/customer_home.html', context)

@login_required(login_url='customer_login')
def custom_logout_view(request):
    clear_messages(request)
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home page

def home(request):
    clear_messages(request)
    return render(request, 'home.html')

# View Customer Profile
@login_required(login_url='customer_login')
def view_customer_profile(request):
    clear_messages(request)
    customer = get_object_or_404(Customer, user=request.user)
    addresses = customer.addresses.all()
    payments = customer.payments.all()

    return render(request, 'customers/view_profile.html', {
        'customer': customer,
        'addresses': addresses,
        'payments': payments
    })

# Add Address
@login_required(login_url='customer_login')
def add_address(request):
    clear_messages(request)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user.customer
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('view_customer_profile')
    else:
        form = AddressForm()
    return render(request, 'customers/add_address.html', {'form': form})

# Add Payment Information
@login_required(login_url='customer_login')
def add_payment_information(request):
    clear_messages(request)
    if request.method == 'POST':
        form = PaymentInformationForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = request.user.customer
            payment.save()
            messages.success(request, 'Payment information added successfully!')
            return redirect('view_customer_profile')
    else:
        form = PaymentInformationForm()
    return render(request, 'customers/add_payment.html', {'form': form})


@login_required(login_url='customer_login')
def update_customer_profile(request):
    clear_messages(request)
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        form = CustomerProfileUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('view_customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerProfileUpdateForm(instance=customer)

    return render(request, 'customers/update_profile.html', {'form': form})


@login_required(login_url='customer_login')
def change_password(request):
    clear_messages(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session hash to keep the user logged in after changing the password
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('view_customer_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'customers/change_password.html', {'form': form})

def browse_products_by_category(request):
    # Retrieve all available categories from the Product model
    categories = Product.CATEGORY_CHOICES
    # Get the selected category from the query parameters (default to the first category)
    selected_category = request.GET.get('category', categories[0][0])
    
    # Filter products based on the selected category
    products = Product.objects.filter(category=selected_category)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'products': products,
    }
    return render(request, 'customers/browse_products_by_category.html', context)

# View product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'customers/product_detail.html', {'product': product})


@login_required(login_url='customer_login')
def create_subscription_box(request):
    if request.method == 'POST':
        form = SubscriptionBoxForm(request.user, request.POST)
        if form.is_valid():
            subscription_box = form.save(commit=False)
            subscription_box.customer = request.user
            subscription_box.save()
            messages.success(request, 'Subscription box created successfully!')
            return redirect('customer_home')
    else:
        form = SubscriptionBoxForm(request.user)
    return render(request, 'customers/create_subscription_box.html', {'form': form})

# Add a product to a subscription box
@login_required(login_url='customer_login')
def add_product_to_box(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = AddProductToBoxForm(request.user, request.POST)
        if form.is_valid():
            box = form.cleaned_data['box']
            # Check if the product is already in the selected box
            if BoxProduct.objects.filter(box=box, product=product).exists():
                messages.warning(request, f'Product "{product.name}" is already in the box "{box.name}".')
            else:
                BoxProduct.objects.create(box=box, product=product)
                messages.success(request, f'Product "{product.name}" added to box "{box.name}" successfully!')
            return redirect('product_detail', product_id=product_id)
    else:
        form = AddProductToBoxForm(request.user)
    return render(request, 'customers/add_product_to_box.html', {'form': form, 'product': product})


# View all subscription boxes
@login_required(login_url='customer_login')
def view_subscriptions(request):
    boxes = SubscriptionBox.objects.filter(customer=request.user)
    return render(request, 'customers/view_subscriptions.html', {'boxes': boxes})


# Activate/Deactivate a subscription box
@login_required(login_url='customer_login')
def toggle_subscription_status(request, box_id):
    box = get_object_or_404(SubscriptionBox, id=box_id, customer=request.user)
    box.is_active = not box.is_active  # Toggle the status
    box.save()
    status = 'activated' if box.is_active else 'deactivated'
    messages.success(request, f'Subscription box "{box.name}" has been {status}.')
    return redirect('view_subscriptions')

# Delete a product from a subscription box
@login_required(login_url='customer_login')
def delete_product_from_box(request, box_id, product_id):
    box = get_object_or_404(SubscriptionBox, id=box_id, customer=request.user)
    box_product = get_object_or_404(BoxProduct, box=box, product_id=product_id)
    box_product.delete()
    messages.success(request, 'Product removed from the subscription box.')
    return redirect('view_subscriptions')


# Add comment and rating
@login_required(login_url='customer_login')
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.customer = request.user.customer
            comment.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductCommentForm()
    return render(request, 'customers/add_comment.html', {'form': form, 'product': product})

# Raise a question about the product
@login_required(login_url='customer_login')
def add_question(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.product = product
            question.customer = request.user.customer
            question.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductQuestionForm()
    return render(request, 'customers/add_question.html', {'form': form, 'product': product})