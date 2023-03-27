from django import forms
from .models import Genre


class GenreChoiceField(forms.ChoiceField):
    def __init__(self, choices=()):
        super().__init__(choices=choices)
        current_choices = self.choices
        self.choices = (('alphabetical', 'Alphabetically'), ('popularity', 'By popularity'))
        self.choices += current_choices


class HomeForm(forms.Form):
    genre = GenreChoiceField(choices=[])


class MatchForm(forms.Form):
    genre = GenreChoiceField(choices=[])

    def __init__(self, category, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices += [(x.pk, x.name) for x in Genre.objects.filter(category=category)]
