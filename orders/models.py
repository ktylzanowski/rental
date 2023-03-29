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


class Shipping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_method = models.CharField(max_length=100)
    if_paid = models.BooleanField(default=False, null=False)
    postage = models.IntegerField(null=False)
    quantity_of_items = models.IntegerField(null=False)


class Order(models.Model):
    status_types = [
        ("Ordered", "Ordered"),
        ("Sent", "Sent"),
        ("Delivered", "Delivered"),
        ("Extended", "Extended"),
        ("Returned", "Returned"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    deadline = models.DateTimeField(null=True)
    return_date = models.DateTimeField(null=True)
    status = models.CharField(choices=status_types, default="Ordered", max_length=100)
    total = models.IntegerField(null=False)
    debt = models.IntegerField(null=True, default=0)
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
    if_extended = models.BooleanField(default=False, null=True, blank=True)
    number_of_extensions = models.IntegerField(default=0, null=True, blank=True)

    def total_cost(self):
        return (self.number_of_extensions * self.total) + self.total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=False, blank=False, default=15)


