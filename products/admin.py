from django.contrib import admin
from .models import Rental, Book, CD, Film, Genre, ProductIndex
from .forms_admin import BookForm, FilmForm, CDForm
from django.urls import reverse
from django.utils.html import format_html


class ItemInline(admin.StackedInline):
    model = ProductIndex
    extra = 0


@admin.register(ProductIndex)
class ProductIndex(admin.ModelAdmin):
    list_display = ['inventory_number', 'product', 'rental_link', 'is_available']
    list_filter = ['rental__name', 'is_available']
    search_fields = ['inventory_number']

    def rental_link(self, obj):
        related_obj = obj.rental
        url = reverse('admin:products_rental_change', args=[related_obj.id])
        return format_html('<a href="{}">{}</a>', url, related_obj)

    rental_link.short_description = 'Product'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']

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


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    list_filter = ['genre', 'is_available']
    search_fields = ['title']
    exclude = ['popularity']
    inlines = [ItemInline]
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
