from polymorphic.models import PolymorphicModel
from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class Product(PolymorphicModel):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='product', default=None)
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
        ('Disco', 'Disco'),
        ('Electronic music', 'Electronic music'),
        ('Rap', 'Rap'),
        ('Reggae', 'Reggae'),
        ('Rock', 'Rock'),
        ('Pop', 'Pop'),
    )
    band = models.CharField(max_length=100, null=False, blank=False)
    tracklist = models.TextField(max_length=500, null=False, blank=False)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, null=False, blank=False)

    def full_clean(self, exclude, validate_unique=True, validate_constraints=True):
        if CD.objects.filter(genre=self.genre, tracklist=self.tracklist).exists():
            ValueError('Within one genre, we cannot offer two albums with the same track list')
        try:
            cds = CD.objects.filter(band=self.band)
            tab = []
            for cd in cds:
                tab.append(cd.genre)
            set(tab)
            if self.genre not in tab and len(tab) > 2:
                ValueError('CDs of a given band can only be offered in two genres')
        except ObjectDoesNotExist:
            pass


class Book(Product):
    GENRE_CHOICES = (
        ('Biography', 'Biography'),
        ('Criminal', 'Criminal'),
        ('Fantasy', 'Fantasy'),
        ('Historical Novel', 'Historical Novel'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
    )
    author = models.CharField(max_length=100, null=False, blank=False)
    isbn = models.CharField(max_length=100, null=False, blank=False, unique=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, null=False, blank=False)

    def full_clean(self, exclude, validate_unique=True, validate_constraints=True):
        if Book.objects.filter(author=self.author, title=self.title, genre=self.genre).exists():
            raise ValueError("Author, title and genre must not be repeated")


class Film(Product):
    GENRE_CHOICES = (
        ('Adventure', 'Adventure'),
        ('Animated', 'Animated'),
        ('Comedy', 'Comedy'),
        ('Horror', 'Horror'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
    )
    director = models.CharField(max_length=100, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, null=False, blank=False)

    def full_clean(self, exclude, validate_unique=True, validate_constraints=True):
        if Film.objects.filter(director=self.director, title=self.title, duration=self.duration).exists():
            raise ValueError("If the director and title are repeated, the duration must differ")

        genres = ('Comedy', 'Adventure', 'Romance', 'Horror', 'Thriller', 'Animated')
        tab = []
        for genre in genres:
            tab.append(len(Film.objects.filter(genre=genre)))
            if self.genre == genre:
                tab[-1] += 1
        if max(tab) - min(tab) > 3:
            ValueError('The numbers of different films of a given genre within the entire collection may vary by 3')

