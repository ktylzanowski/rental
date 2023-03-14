from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from accounts.models import MyUser
from products.models import Product, Book, CD, Film
from .forms import OrderStatus


class AdminPanel(View):

    def get(self, request):
        number_of_books = len(Book.objects.all())
        number_of_cds = len(CD.objects.all())
        number_of_films = len(Film.objects.all())
        number_of_all_products = len(Product.objects.all())

        number_of_ordered = len(Order.objects.filter(status="Ordered"))
        number_of_sent = len(Order.objects.filter(status="Sent"))
        number_of_delivered = len(Order.objects.filter(status="Delivered"))
        number_of_extended = len(Order.objects.filter(status="Extended"))
        number_of_returned = len(Order.objects.filter(status="Returned"))

        number_of_carts = len(Cart.objects.all())
        number_of_items_in_carts = len(CartItem.objects.all())

        number_of_users = len(MyUser.objects.all())

        context = {'number_of_books': number_of_books, 'number_of_cds': number_of_cds,
                   'number_of_films': number_of_films, 'number_of_all_products': number_of_all_products,
                   'number_of_ordered': number_of_ordered, 'number_of_sent': number_of_sent,
                   'number_of_delivered': number_of_delivered, 'number_of_extended': number_of_extended,
                   'number_of_returned': number_of_returned, 'number_of_carts': number_of_carts,
                   'number_of_items_in_carts': number_of_items_in_carts, 'number_of_users': number_of_users}

        return render(request, 'adminpanel/adminpanel.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'adminpanel/ordersListView.html'
    ordering = ['-pk']

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET:
            qs = qs.filter(status=self.request.GET['status'])

        return qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['order_status'] = OrderStatus
        return data


class OrderDetailView(DetailView):
    model = Order
    template_name = 'adminpanel/detailview/order.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(order=kwargs['object'])
        data['order_status'] = OrderStatus
        data['order_items'] = order_items
        return data


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
        data['books'] = Product.objects.filter(category='book')
        data['cds'] = Product.objects.filter(category='cd')
        data['films'] = Product.objects.filter(category='film')
        return data


class BookCreateView(CreateView):
    model = Book
    template_name = 'adminpanel/createProduct.html'
    success_url = '/adminpanel/'

    fields = [
        'title',
        'image',
        'quantity',
        'price',
        'author',
        'isbn',
        'genre',
    ]

    def form_valid(self, form):
        books = Book.objects.all()
        for book in books:
            if book.author == self.request.POST['author'] and book.title == self.request.POST['title'] \
                    and book.genre == self.request.POST['genre']:
                return redirect('BookCreateView')
        return super().form_valid(form)


class CDCreateView(CreateView):
    model = CD
    template_name = 'adminpanel/createProduct.html'
    success_url = '/adminpanel/'

    fields = [
        'title',
        'image',
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
        'quantity',
        'price',
        'director',
        'duration',
        'genre',
    ]

    def form_valid(self, form):
        films = Film.objects.all()
        for film in films:
            if film.director == self.request.POST['director'] and film.title == self.request.POST['title'] \
                    and str(film.duration) == (self.request.POST['duration']):
                return redirect('FilmCreateView')
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminpanel/productDelete.html'
    success_url = '/adminpanel/products'


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'adminpanel/productUpdate.html'
    success_url = '/adminpanel/products'
    fields = [
        'title',
        'image',
        'quantity',
        'price',
        'author',
        'isbn',
        'genre',
    ]


class CDUpdateView(UpdateView):
    model = CD
    template_name = 'adminpanel/productUpdate.html'
    success_url = '/adminpanel/products'
    fields = [
        'title',
        'image',
        'quantity',
        'price',
        'band',
        'tracklist',
        'genre',
    ]


class FilmUpdateView(UpdateView):
    model = Film
    template_name = 'adminpanel/productUpdate.html'
    success_url = '/adminpanel/products'
    fields = [
        'title',
        'image',
        'quantity',
        'price',
        'director',
        'duration',
        'genre',
    ]


class UserDeleteView(DeleteView):
    model = MyUser
    template_name = 'adminpanel/productDelete.html'
    success_url = '/adminpanel/users'


class UserUpdateView(UpdateView):
    model = MyUser
    template_name = 'adminpanel/productUpdate.html'
    success_url = '/adminpanel/users'
    fields = [
        'email',
        'first_name',
        'last_name',
        'phone',
        'city',
        'zip_code',
        'street',
        'building_number',
        'apartment_number',
        'is_active',
        'is_admin',
        'is_staff',
    ]


class ChangeOrderStatus(View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = self.request.POST['status']
        if self.request.POST['status'] == 'Extended':
            items = OrderItem.objects.filter(order=order)
            for item in items:
                item.debt += item.price
                item.save()
        order.save()
        return redirect('OrdersListView')
