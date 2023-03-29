from django.contrib import admin
from .models import Payment, Shipping, Order, OrderItem


admin.site.register(Payment)
admin.site.register(Shipping)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['user', 'order_date', 'deadline', 'status', 'total', 'debt', 'shipping']
    list_filter = ['status', 'if_extended']
    exclude = ['order_date', 'deadline', 'return_date', 'total', 'payment', 'shipping', 'if_extended', 'number_of_extensions']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['product', 'order', 'user', 'price']
    list_filter = ['order', 'user']
