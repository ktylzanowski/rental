from django.views.generic import ListView, DetailView
from products.models import Product, Book, CD, Film
from . import forms
from .mixin import HomeMixin
from cart.cart import Cart


class Home(HomeMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.MatchForm
        return data


class BookListView(HomeMixin, ListView):
    model = Book

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.MatchForm(category="book")
        return data


class FilmListView(HomeMixin, ListView):
    model = Film

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.MatchForm(category="film")
        return data


class CDListView(HomeMixin, ListView):
    model = CD

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.MatchForm(category="cd")
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detailview.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        car = cart.check_if_in_the_same_rental(kwargs['object'])
        data['cartobject'] = car

        return data




