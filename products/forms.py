from .models import CD, Film, Genre, Product, Book
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class MatchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['genre']

    def __init__(self, category=False, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [('', 'Choose')] + \
                                       [('alphabetical', 'Alphabetically'), ('popularity', 'By popularity')]
        if category:
            self.fields['genre'].choices += [(x.pk, x.name) for x in Genre.objects.filter(category=category)]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='book')]

    def clean(self):
        def whether_changed():
            try:
                genre = Genre.objects.get(pk=self.initial['genre'])

                return self.initial['author'] == self.cleaned_data['author'] \
                    and self.initial['title'] == self.cleaned_data['title'] \
                    and genre.name == str(self.cleaned_data['genre'])
            except KeyError:
                return False

        if not whether_changed() and Book.objects.filter(author=self.cleaned_data['author'],
                                                         title=self.cleaned_data['title'],
                                                         genre=self.cleaned_data['genre']).exists():
            raise ValueError("Author, title and genre must not be repeated")
        return self.cleaned_data


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='film')]

    def clean(self):

        def whether_changed():
            try:
                return self.initial['director'] == self.cleaned_data['director'] \
                       and self.initial['title'] == self.cleaned_data['title'] \
                       and self.initial['duration'] == self.cleaned_data['duration']
            except KeyError:
                return False

        def number_genres_in_collection_differ_max_3():
            genres = [genre for genre in Genre.objects.filter(category='film')]
            quantity = []
            for genre in genres:
                quantity.append(len(Film.objects.filter(genre=genre)))
                if self.cleaned_data['genre'] == genre:
                    quantity[-1] += 1
            if max(quantity) - min(quantity) > 3:
                return True

        if not whether_changed() and Film.objects.filter(director=self.cleaned_data['director'],
                                                         title=self.cleaned_data['title'],
                                                         duration=self.cleaned_data['duration']).exists():
            raise ValueError("If the director and title are repeated, the duration must differ")

        if number_genres_in_collection_differ_max_3():
            raise ValueError(
                'The numbers of different films of a given genre within the entire collection may vary by 3')

        return self.cleaned_data


class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CDForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='cd')]

    def clean(self):
        def whether_changed():
            try:
                genre = Genre.objects.get(pk=self.initial['genre'])
                return genre.name == str(self.cleaned_data['genre']) \
                       and self.initial['tracklist'] == self.cleaned_data['tracklist']
            except KeyError:
                return False

        def band_has_more_genres_than_2():
            try:
                cds = CD.objects.filter(band=self.cleaned_data['band'])
                tab = []
                for cd in cds:
                    tab.append(cd.genre)
                set(tab)
                if self.cleaned_data['genre'] not in tab and len(tab) > 2:
                    return True
            except ObjectDoesNotExist:
                return False

        if not whether_changed() and CD.objects.filter(
                genre=self.cleaned_data['genre'],
                tracklist=self.cleaned_data['tracklist']).exists():
            raise ValueError('Within one genre, we cannot offer two albums with the same track list')

        if band_has_more_genres_than_2():
            raise ValueError('CDs of a given band can only be offered in two genres')

        return self.cleaned_data
