from django import forms
from .models import Order


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeSection(forms.Form):
    t1 = forms.DateField(widget=DateInput)
    t2 = forms.DateTimeField(widget=DateInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.fields['status'].initial != 'Extended' and self.cleaned_data['status'] == 'Extended':
            self.cleaned_data['debt'] += self.cleaned_data['total']
            self.cleaned_data['number_of_extensions'] += 1
            self.cleaned_data['if_extended'] = True
        return cleaned_data


