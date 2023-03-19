from django import forms
from orders.models import Order


class OrderStatus(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
