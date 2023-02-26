from django.contrib import admin
from .models import Payment, Shipping, ShippingMethod, Order, OrderItem


admin.site.register(Payment)
admin.site.register(ShippingMethod)
admin.site.register(Shipping)
admin.site.register(Order)
admin.site.register(OrderItem)
