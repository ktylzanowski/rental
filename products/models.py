from polymorphic.models import PolymorphicModel
from django.db import models
from django.urls import reverse


class Product(PolymorphicModel):
    CHOICES_CATEGORY = (
        ('book', 'Book'),
        ('cd', 'CD'),
        ('film', 'Film'),
    )

    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='product', default=None)
    category = models.CharField(choices=CHOICES_CATEGORY, max_length=20, blank=True, null=False)
    quantity = models.IntegerField(null=False)
    is_available = models.BooleanField(default=True, null=False)
    price = models.IntegerField(null=False, blank=False, default=15)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("ProductDetail", args=[str(self.pk)])

    @property
    def model_name(self):
        return self._meta.model_name


class Rental(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    zip_code = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    building_number = models.CharField(max_length=10, null=False, blank=False)
    apartment_number = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.name

class CD(Product):
    GENRE_CHOICES = (
        ('Rock', 'Rock'),
        ('Pop', 'Pop'),
        ('Reggae', 'Reggae'),
        ('Disco', 'Disco'),
        ('Rap', 'Rap'),
        ('Electronic music', 'Electronic music'),
    )
    band = models.CharField(max_length=100, null=False, blank=False)
    tracklist = models.TextField(max_length=500, null=False, blank=False)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, null=False, blank=False)


class Book(Product):
    GENRE_CHOICES = (
        ('Fantasy', 'Fantasy'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Romance', 'Romance'),
        ('Historical Novel', 'Historical Novel'),
        ('Horror', 'Horror'),
        ('Criminal', 'Criminal'),
        ('Biography', 'Biography'),
    )
    author = models.CharField(max_length=100, null=False, blank=False)
    isbn = models.CharField(max_length=100, null=False, blank=False)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, null=False, blank=False)


class Film(Product):
    GENRE_CHOICES = (
        ('Comedy', 'Comedy'),
        ('Adventure', 'Adventure'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
        ('Thriller', 'Thriller'),
        ('Animated', 'Animated'),
    )
    director = models.CharField(max_length=100, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, null=False, blank=False)
