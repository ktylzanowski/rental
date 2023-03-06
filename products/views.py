from django.views.generic import ListView, View
from products.models import Product, Category, Book, Film, CD
from django.shortcuts import redirect, render
from cart.models import Cart, CartItem
from django.contrib import messages
from . import forms


class Home(ListView):
    model = Product
    template_name = 'products/home.html'
    ordering = ['-pk']


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        context = {'object': product}
        return render(request, "products/detailview.html", context)

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
            if item.product.title == added_item.title:
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


class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'products/home.html'

    def get_queryset(self):
        qs = super().get_queryset()
        cat = Category.objects.get(name=self.kwargs['cats'])
        qs = qs.filter(category=cat)
        if self.request.GET and self.request.GET['genre'] == 'alphabetical':
            qs = qs.filter(category=cat).order_by('title')
        elif self.request.GET and self.request.GET['genre'] == 'popularity':
            qs = qs.filter(category=cat).order_by('popularity')
        elif self.request.GET and self.kwargs['cats'] == 'Book':
            qs = Book.objects.filter(genre=self.request.GET['genre'])
        elif self.request.GET and self.kwargs['cats'] == 'CD':
            qs = CD.objects.filter(genre=self.request.GET['genre'])
        elif self.request.GET and self.kwargs['cats'] == 'Film':
            qs = Film.objects.filter(genre=self.request.GET['genre'])
        return qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.kwargs['cats'] == 'Book':
            data['form'] = forms.BookGenreForm
        elif self.kwargs['cats'] == 'CD':
            data['form'] = forms.CDGenreForm
        elif self.kwargs['cats'] == 'Film':
            data['form'] = forms.FilmGenreForm
        data['cats'] = True
        return data
