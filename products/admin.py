from django.contrib import admin
from .models import Rental, Book, CD, Film

admin.site.register(Rental)
admin.site.register(Book)
admin.site.register(CD)
admin.site.register(Film)

