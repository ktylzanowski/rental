from django.contrib import admin
from .models import CD, Book, Film, Order, OrderItem, Category

admin.site.register(CD)
admin.site.register(Book)
admin.site.register(Film)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
