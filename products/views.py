from django.views.generic import ListView, DetailView
from products.models import Product, Book, CD, Film
from . import forms
from .mixin import HomeMixin

class Home(HomeMixin, ListView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.HomeForm
        return data


class BookListView(HomeMixin, ListView):
    model = Book

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.BookGenreForm
        return data


class FilmListView(HomeMixin, ListView):
    model = Film

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.FilmGenreForm
        return data


class CDListView(HomeMixin, ListView):
    model = CD

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = forms.CDGenreForm
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detailview.html"








