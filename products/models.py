from polymorphic.models import PolymorphicModel
from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Product(PolymorphicModel):

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='product', default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(null=False)
    is_available = models.BooleanField(default=True, null=False)
    price = models.IntegerField(null=False, default=15)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("ProductDetail", args=[str(self.pk)])

    @property
    def model_name(self):
        return self._meta.model_name


class CD(Product):
    band = models.CharField(max_length=100)
    tracklist = models.TextField(max_length=500)


class Book(Product):
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)


class Film(Product):
    director = models.CharField(max_length=100)
    duration = models.IntegerField()


class Order(models.Model):
    status_types = [
        ("Ordered", "Ordered"),
        ("Sent", "Sent"),
        ("Delivered", "Delivered"),
        ("Returned", "Returned"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    status = models.CharField(choices=status_types, default="Ordered", max_length=100)
    total = models.IntegerField(null=False)

    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=12, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False, default=None)
    zip_code = models.CharField(max_length=10, null=False, blank=False, default=None)
    street = models.CharField(max_length=255, null=False, blank=False, default=None)
    building_number = models.CharField(max_length=10, null=False, blank=False, default=None)
    apartment_number = models.CharField(max_length=10, null=False, blank=False, default=None)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

