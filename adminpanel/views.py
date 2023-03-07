from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView
from orders.models import Order
from cart.models import Cart, CartItem
from accounts.models import MyUser
from products.models import Product, Book, CD, Film


class AdminPanel(View):

    def get(self, request):
        orders = Order.objects.order_by('-order_date')[:5]
        carts = Cart.objects.filter()[:5]
        number_of_books = len(Book.objects.all())
        number_of_cds = len(CD.objects.all())
        number_of_films = len(Film.objects.all())
        number_of_all_products = len(Product.objects.all())

        number_of_ordered = len(Order.objects.filter(status="Ordered"))
        number_of_sent = len(Order.objects.filter(status="sent"))
        number_of_delivered = len(Order.objects.filter(status="Delivered"))
        number_of_extended = len(Order.objects.filter(status="Extended"))
        number_of_returned = len(Order.objects.filter(status="Returned"))

        context = {'orders': orders, 'carts': carts, 'number_of_books': number_of_books, 'number_of_cds': number_of_cds,
                   'number_of_films': number_of_films, 'number_of_all_products': number_of_all_products, 'number_of_ordered':
                   number_of_ordered, 'number_of_sent': number_of_sent, 'number_of_delivered': number_of_delivered,
                   'number_of_extended': number_of_extended, 'number_of_returned': number_of_returned}

        return render(request, 'adminpanel/adminpanel.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'adminpanel/ordersListView.html'
    ordering = ['-pk']


class OrderDetailView(DetailView):
    model = Order
    template_name = 'adminpanel/detailview/order.html'


class CartListView(ListView):
    model = Cart
    template_name = 'adminpanel/cartListView.html'
    ordering = ['-pk']


class CartDetailView(DetailView):
    model = Cart
    template_name = 'adminpanel/detailview/cart.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user_cart = Cart.objects.get(user=self.request.user)
        data['cart_items'] = CartItem.objects.filter(cart=user_cart)
        return data


class UsersListView(ListView):
    model = MyUser
    template_name = 'adminpanel/usersListView.html'
    ordering = ['-pk']


class ProductsListView(ListView):
    model = Product
    template_name = 'adminpanel/productListView.html'
    ordering = ['-pk']

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['books'] = Book.objects.all()
        data['cds'] = CD.objects.all()
        data['films'] = Film.objects.all()
        return data


class BookCreateView(CreateView):
    model = Book
    template_name = 'adminpanel/createProduct.html'
    success_url = '/adminpanel/'

    fields = [
        'title',
        'image',
        'category',
        'quantity',
        'price',
        'author',
        'isbn',
        'genre',
    ]


class CDCreateView(CreateView):
    model = CD
    template_name = 'adminpanel/createProduct.html'
    success_url = '/adminpanel/'

    fields = [
        'title',
        'image',
        'category',
        'quantity',
        'price',
        'band',
        'tracklist',
        'genre',
    ]


class FilmCreateView(CreateView):
    model = Film
    template_name = 'adminpanel/createProduct.html'
    success_url = '/adminpanel/'

    fields = [
        'title',
        'image',
        'category',
        'quantity',
        'price',
        'director',
        'duration',
        'genre',
    ]


class BookDeleteView(DeleteView):
    model = Book
    success_url = '/adminpanel/'
