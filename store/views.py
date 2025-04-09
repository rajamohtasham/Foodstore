from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Order, OrderItem, CartItem, UserProfile
from .forms import UserProfileForm
import requests

# ✅ Home Page (Product Listing)
def home(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'products': products, 'categories': categories, 'query': query})

# ✅ Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# ✅ Products by Category
def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'store/category_products.html', {
        'products': products, 
        'category': category, 
        'categories': categories
    })

# ✅ Categories Page (Newly Added)
def categories(request):
    categories = Category.objects.all()
    return render(request, 'store/categories.html', {'categories': categories})

# ✅ Cart View
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_data': cart_items, 'total_price': total_price})

# ✅ Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, 
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart')

# ✅ Update Cart (Increase/Decrease Quantity)
@login_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, user=request.user, product=product)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

    return redirect("cart")

# ✅ Remove Item from Cart
@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart')

# ✅ Checkout
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items:
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id', '')

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            address=address,
            phone=phone,
            total_price=total_price,
            payment_method=payment_method,
            transaction_id=transaction_id
        )

        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

        cart_items.delete()

        return render(request, 'store/order_confirmation.html', {'order': order})

    return render(request, 'store/checkout.html')

# ✅ Order History (User-Specific)
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


# ✅ User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# ✅ User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

# ✅ User Logout
def logout_view(request):
    logout(request)
    return redirect('home')

# ✅ Profile View
@login_required
def view_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'store/view_profile.html', {'user_profile': user_profile})

# ✅ Edit Profile
@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'store/edit_profile.html', {'form': form})

# ✅ Contact Form (Web3Forms API)
def contact(request):
    if request.method == "POST":
        access_key = "178a59ab-a8a0-4d12-95e5-b57a4f38b727"
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        data = {"access_key": access_key, "name": name, "email": email, "message": message}
        response = requests.post("https://api.web3forms.com/submit", json=data)
        result = response.json()

        return render(request, "store/contact.html", {"result": "Message sent!"} if result.get("success") else {"form_error": "An error occurred."})

    return render(request, "store/contact.html")

def order_success(request):
    return render(request, 'store/order_success.html')
