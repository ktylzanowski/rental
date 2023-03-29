from django.contrib import admin
from .models import Rental, Book, CD, Film, Genre
from .forms_admin import BookForm, FilmForm, CDForm


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    form = BookForm


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    form = FilmForm


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    form = CDForm


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'zip_code', 'street', 'building_number', 'apartment_number']
    list_filter = ['city']
    search_fields = ['name']