from django.views.generic import ListView, DetailView, View
from products.models import Product, Book, CD, Film
from django.shortcuts import redirect
from cart.models import Cart, CartItem
from django.contrib import messages
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


class AddToCart(View):

    def post(self, request, pk):

        if not request.user.is_authenticated:
            messages.success(request, "You must be logged in")
            return redirect('Login')

        cart, created = Cart.objects.get_or_create(
            user=request.user,
        )
        cart.save()

        added_item = Product.objects.get(id=pk)
        added_item.popularity += 1
        added_item.save()

        item_in_cart = CartItem.objects.filter(cart=cart)

        for item in item_in_cart:
            if item.product == added_item:
                messages.success(request, "It's already in the basket")
                return redirect('ProductDetail', pk=pk)

        new_item_in_cart = CartItem.objects.create(
            product=added_item,
            cart=cart,
        )

        new_item_in_cart.save()

        added_item.quantity -= 1

        if added_item.quantity == 0:
            added_item.is_available = False
        added_item.save()

        messages.success(request, "Add to cart")
        return redirect('home')






