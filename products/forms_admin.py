from .models import CD, Film, Genre, Product
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='book')]


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='film')]


class CDForm(forms.ModelForm):

    class Meta:
        model = CD
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CDForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = [(x.pk, x.name) for x in Genre.objects.filter(category='cd')]
