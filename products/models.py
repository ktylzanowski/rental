from polymorphic.models import PolymorphicModel
from django.db import models
from django.conf import settings


class Product(PolymorphicModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='product', default=None)

    def __str__(self):
        return str(self.title)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
