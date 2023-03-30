from .models import CD, Film, Genre, Product, Book
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class BookForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='book')]

    def clean(self):
        if BookForm.has_changed(self) and Book.objects.filter(author=self.cleaned_data['author'],
                                                              title=self.cleaned_data['title'], genre=self.cleaned_data['genre']).exists():
            raise ValueError("Author, title and genre must not be repeated")


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='film')]

    def clean(self):
        if FilmForm.has_changed(self) and Film.objects.filter(
                                                            director=self.cleaned_data['director'],
                                                            title=self.cleaned_data['title'],
                                                            duration=self.cleaned_data['duration']).exists():
            raise ValueError("If the director and title are repeated, the duration must differ")


class CDForm(forms.ModelForm):

    class Meta:
        model = CD
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CDForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='cd')]

    def clean(self):
        if CDForm.has_changed(self) \
                and CD.objects.filter(genre=self.cleaned_data['genre'], tracklist=self.cleaned_data['tracklist']).exists():
            raise ValueError('Within one genre, we cannot offer two albums with the same track list')
        try:
            cds = CD.objects.filter(band=self.cleaned_data['band'])
            tab = []
            for cd in cds:
                tab.append(cd.genre)
            set(tab)
            if self.cleaned_data['genre'] not in tab and len(tab) > 2:
                raise ValueError('CDs of a given band can only be offered in two genres')
        except ObjectDoesNotExist:
            pass
