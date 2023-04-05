from polymorphic.models import PolymorphicModel
from django.db import models
from django.urls import reverse


class Rental(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    zip_code = models.CharField(max_length=100, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    building_number = models.CharField(max_length=10, null=False, blank=False)
    apartment_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    CATEGORY_CHOICES = (('book', 'Book'),
                        ('cd', 'CD'),
                        ('film', 'Film'),)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return str(self.name)


class Product(PolymorphicModel):
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='product', blank=False, null=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=0)
    is_available = models.BooleanField(default=True, null=False)
    price = models.IntegerField(null=False, blank=False, default=15)
    popularity = models.IntegerField(default=0)

    def save(self):
        if self.quantity == 0:
            self.is_available = False
        else:
            self.is_available = True

        super(Product, self).save()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("ProductDetail", kwargs={"pk": str(self.pk)})

    @property
    def model_name(self):
        return self._meta.model_name


class ProductIndex(models.Model):
    inventory_number = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.inventory_number)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product.quantity += 1
            self.product.save()
        super(ProductIndex, self).save(*args, **kwargs)


class Book(Product):
    author = models.CharField(max_length=100, null=False, blank=False)
    isbn = models.CharField(max_length=100, null=False, blank=False, unique=True)


class Film(Product):
    director = models.CharField(max_length=100, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)


class CD(Product):
    band = models.CharField(max_length=100, null=False, blank=False)
    tracklist = models.TextField(max_length=500, null=False, blank=False)
