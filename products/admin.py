from django.contrib import admin
from .models import CD, Book, Film, Order, OrderItem, Category, Payment, Shipping, ShippingMethod

admin.site.register(CD)
admin.site.register(Book)
admin.site.register(Film)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(ShippingMethod)
admin.site.register(Shipping)