from django.contrib import admin
from .models import Rental, Book, CD, Film, Genre

admin.site.register(Rental)
admin.site.register(Book)
admin.site.register(CD)
admin.site.register(Film)
admin.site.register(Genre)
