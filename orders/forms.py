from django import forms


class CategoryForm(forms.Form):
    CATEGORY_CHOICES = (
        ('book', 'Book'),
        ('cd', 'CD'),
        ('film', 'Film'),
    )

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
