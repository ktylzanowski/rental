from django.contrib import admin
from .models import CD, Book, Film, Rental

admin.site.register(CD)
admin.site.register(Book)
admin.site.register(Film)
admin.site.register(Rental)
