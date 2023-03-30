from django.contrib import admin
from .models import Payment, Shipping, Order, OrderItem
from .forms import OrderForm
from django.urls import reverse
from django.utils.html import format_html


class ItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['pk', 'user', 'order_date', 'deadline', 'status', 'payment_link', 'total', 'debt', 'shipping_link']
    list_filter = ['status', 'if_extended']
    fieldsets = (
        ('Order', {'fields': ('user', 'order_date', 'deadline', 'return_date', 'status',
                              'total', 'debt', 'payment', 'shipping', 'number_of_extensions', 'if_extended')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone',
                                      'city', 'zip_code', 'street', 'building_number', 'apartment_number')}),
    )

    readonly_fields = ['order_date', 'deadline', 'return_date', 'payment', 'shipping']
    search_fields = ('pk',)
    inlines = [ItemInline]

    form = OrderForm

    def payment_link(self, obj):
        related_obj = obj.payment
        url = reverse('admin:orders_payment_change', args=[related_obj.id])
        return format_html('<a href="{}">{}</a>', url, related_obj)

    def shipping_link(self, obj):
        related_obj = obj.shipping
        url = reverse('admin:orders_shipping_change', args=[related_obj.id])
        return format_html('<a href="{}">{}</a>', url, related_obj)

    payment_link.short_description = 'Payment'
    shipping_link.short_description = 'Shipping'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ('pk',)
    list_display = ['pk', 'product', 'order', 'user', 'price']
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
