from django import forms
from .models import Book, CD, Film


class GenreChoiceField(forms.ChoiceField):
    def __init__(self, choices=()):
        super().__init__(choices=choices)
        current_choices = self.choices
        self.choices = (('alphabetical', 'Alphabetically'), ('popularity', 'By popularity'))
        self.choices += current_choices


class HomeForm(forms.Form):
    choices = ()
    genre = GenreChoiceField(choices=choices)


class BookGenreForm(forms.ModelForm):
    genre = GenreChoiceField(choices=Book.GENRE_CHOICES)

    class Meta:
        model = Book
        fields = ('genre',)


class CDGenreForm(forms.ModelForm):
    genre = GenreChoiceField(choices=CD.GENRE_CHOICES)

    class Meta:
        model = CD
        fields = ('genre',)


class FilmGenreForm(forms.ModelForm):
    genre = GenreChoiceField(choices=Film.GENRE_CHOICES)

    class Meta:
        model = Film
        fields = ('genre',)
