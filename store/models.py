from django.db import models
from django.contrib.auth.models import User
import os


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"


### 🔹 **User Profile Model** (Newly Added)
def user_profile_path(instance, filename):
    return f"profile_pics/user_{instance.user.id}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=user_profile_path, default='profile_pics/default.png', blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


### 🔹 **Cart Item Model**
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.user.username})"


### 🔹 **Order Model**
class Order(models.Model):
    PAYMENT_METHODS = [
        ('Easypaisa', 'Easypaisa'),
        ('JazzCash', 'JazzCash'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]
    ORDER_STATUS = [
        ('Received', 'Received'),
        ('Packed', 'Packed'),
        ('Dispatch', 'Dispatch'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="Not Provided")
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='Easypaisa')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)  # ✅ New field
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username if self.user else 'Guest'} - {self.order_status}"


### 🔹 **Order Item Model**
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 🔥 Add default=0.00

    def save(self, *args, **kwargs):
        if not self.price:  # 🔥 Ensure price is set
            self.price = self.product.price * self.quantity  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
