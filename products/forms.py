from django import forms
from .models import Book, CD, Film


class BookGenreForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('genre',)


class CDGenreForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ('genre',)


class FilmGenreForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('genre',)
