from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeSection(forms.Form):
    t1 = forms.DateField(widget=DateInput)
    t2 = forms.DateTimeField(widget=DateInput)
