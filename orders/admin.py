from django.contrib import admin
from .models import Payment, Shipping, Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['pk', 'user', 'order_date', 'deadline', 'status', 'total', 'debt', 'shipping']
    list_filter = ['status', 'if_extended']
    exclude = ['order_date', 'deadline', 'return_date', 'total', 'payment', 'shipping', 'if_extended', 'number_of_extensions']
    search_fields = ('pk',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['product', 'order', 'user', 'price']
    list_filter = ['order', 'user']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'amount_paid']
    list_filter = ['user', 'payment_method']
    search_fields = ('payment_id',)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'shipping_method', 'postage', 'quantity_of_items']
    list_filter = ['shipping_method']
    search_fields = ('pk',)
