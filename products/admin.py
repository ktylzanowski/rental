from django.contrib import admin
from .models import Rental, Book, CD, Film, Genre, ProductIndex
from .forms import BookForm, FilmForm, CDForm


class ItemInline(admin.StackedInline):
    model = ProductIndex
    ordering = ['inventory_number']
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    ordering = ['title']

    inlines = [ItemInline]
    form = BookForm


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    inlines = [ItemInline]

    form = FilmForm
    ordering = ['title']


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    ordering = ['title']

    inlines = [ItemInline]
    form = CDForm


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'zip_code', 'street', 'building_number', 'apartment_number']
    list_filter = ['city']
    search_fields = ['name']
    ordering = ['name']
