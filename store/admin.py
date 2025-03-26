from django.contrib import admin
from .models import Category, Product, Order, OrderItem, UserProfile

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'payment_method', 'payment_status', 'order_status', 'created_at')
    list_filter = ('payment_status', 'order_status', 'payment_method')
    search_fields = ('user__username', 'email', 'phone', 'transaction_id')
    actions = ['mark_as_confirmed', 'mark_as_rejected', 'mark_as_packed', 'mark_as_dispatched', 'mark_as_delivered']

    # ✅ Bulk update Payment Status
    def mark_as_confirmed(self, request, queryset):
        queryset.update(payment_status='Confirmed')
    mark_as_confirmed.short_description = "Mark selected orders as Confirmed"

    def mark_as_rejected(self, request, queryset):
        queryset.update(payment_status='Rejected')
    mark_as_rejected.short_description = "Mark selected orders as Rejected"

    # ✅ Bulk update Order Status
    def mark_as_packed(self, request, queryset):
        queryset.update(order_status='Packed')
    mark_as_packed.short_description = "Mark selected orders as Packed"

    def mark_as_dispatched(self, request, queryset):
        queryset.update(order_status='Dispatch')
    mark_as_dispatched.short_description = "Mark selected orders as Dispatched"

    def mark_as_delivered(self, request, queryset):
        queryset.update(order_status='Delivered')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserProfile)

