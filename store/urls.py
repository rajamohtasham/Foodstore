from django.urls import path
from .views import (
    home, product_detail, category_products, cart, add_to_cart, remove_from_cart, 
    checkout, order_success, order_history, register, login_view, logout_view, 
    custom_logout, update_cart, edit_profile, view_profile, contact
)

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path("order-success/", order_success, name="order_success"),
    path('order-history/', order_history, name='order_history'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),  # ✅ Fixed Duplicate Logout

    path("cart/update/<int:product_id>/", update_cart, name="update_cart"),

    path('profile/', view_profile, name='view_profile'),  # ✅ View Profile
    path('profile/edit/', edit_profile, name='edit_profile'),  # ✅ Edit Profile
    path('contact/', contact, name='contact'),

]
