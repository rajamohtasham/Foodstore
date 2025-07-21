from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    home, product_detail, category_products, cart, add_to_cart, remove_from_cart, 
    checkout, order_success, order_history, register, login_view, logout_view, 
    update_cart, edit_profile, view_profile, contact, categories  # ✅ Added categories view
)

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', category_products, name='category_products'),
    path('categories/', categories, name='categories'),  # ✅ Added this line

    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart, name="update_cart"),
    
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('order-history/', order_history, name='order_history'),

    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # ✅ Removed custom_logout (no need for duplication)

    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    path('contact/', contact, name='contact'),

    path('profile/change-password/', auth_views.PasswordChangeView.as_view(
        template_name='store/change_password.html',
        success_url='/profile/'
    ), name='change_password'),
]
