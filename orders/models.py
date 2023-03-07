from django.db import models
from django.conf import settings
from products.models import Product


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class ShippingMethod(models.Model):
    name = models.CharField(null=False, max_length=100)
    price = models.IntegerField(null=False)

    def __str__(self):
        return str(self.name)


class Shipping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)
    if_paid = models.BooleanField(default=False, null=False)
    postage = models.IntegerField(null=False)
    quantity_of_items = models.IntegerField(null=False)


class Order(models.Model):
    status_types = [
        ("Ordered", "Ordered"),
        ("Sent", "Sent"),
        ("Delivered", "Delivered"),
        ("Returned", "Returned"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True)
    status = models.CharField(choices=status_types, default="Ordered", max_length=100)
    total = models.IntegerField(null=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=False, blank=False)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=False, blank=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False, default=None)
    zip_code = models.CharField(max_length=10, null=False, blank=False, default=None)
    street = models.CharField(max_length=255, null=False, blank=False, default=None)
    building_number = models.CharField(max_length=10, null=False, blank=False, default=None)
    apartment_number = models.CharField(max_length=10, null=True, blank=True, default=None)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=False, blank=False, default=15)
    debt = models.IntegerField(null=True, default=0)