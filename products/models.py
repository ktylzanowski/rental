from polymorphic.models import PolymorphicModel
from django.db import models


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
