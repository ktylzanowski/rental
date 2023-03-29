from django.contrib import admin
from .models import Rental, Book, CD, Film, Genre, Product
from django import forms

admin.site.register(Rental)
admin.site.register(Genre)


class BookForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='book')]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    exclude = ['popularity']
    form = BookForm


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='film')]


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    exclude = ['popularity']
    form = FilmForm


class CDForm(forms.ModelForm):
    list_display = ['title', 'genre', 'price', 'quantity', 'is_available']
    exclude = ['popularity']

    class Meta:
        model = CD
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CDForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='cd')]


@admin.register(CD)
class CDAdmin(admin.ModelAdmin):
    form = CDForm
