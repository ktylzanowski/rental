from django import forms
from .models import Genre
from .models import Product


class MatchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['genre']

    def __init__(self, category=False, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['genre'].choices = (('alphabetical', 'Alphabetically'), ('popularity', 'By popularity'))
        if category:
            self.fields['genre'].choices += [(x.pk, x.name) for x in Genre.objects.filter(category=category)]
