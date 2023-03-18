from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from orders.models import Order
from accounts.models import MyUser
from products.models import Product, Book, CD, Film
from .mixin import StatusMixin, OnlyAdmin


class AdminPanel(OnlyAdmin, View):

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

        number_of_users = len(MyUser.objects.all())

        context = {'number_of_books': number_of_books, 'number_of_cds': number_of_cds,
                   'number_of_films': number_of_films, 'number_of_all_products': number_of_all_products,
                   'number_of_ordered': number_of_ordered, 'number_of_sent': number_of_sent,
                   'number_of_delivered': number_of_delivered, 'number_of_extended': number_of_extended,
                   'number_of_returned': number_of_returned, 'number_of_users': number_of_users}

        return render(request, 'adminpanel/adminpanel.html', context)


class OrderListView(OnlyAdmin, StatusMixin, ListView):
    model = Order
    template_name = 'adminpanel/ordersListView.html'
    ordering = ['-pk']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET:
            qs = qs.filter(status=self.request.GET['status'])
        return qs


class OrderDetailView(OnlyAdmin, StatusMixin, DetailView):
    model = Order
    template_name = 'adminpanel/detailview/order.html'


class UsersListView(OnlyAdmin, ListView):
    model = MyUser
    template_name = 'adminpanel/usersListView.html'
    ordering = ['-pk']


class ProductsListView(OnlyAdmin, ListView):
    model = Product
    template_name = 'adminpanel/productListView.html'
    ordering = ['-pk']

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['books'] = Book.objects.all()
        data['cds'] = CD.objects.all()
        data['films'] = Film.objects.all()
        return data


class BookCreateView(OnlyAdmin, CreateView):
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


class CDCreateView(OnlyAdmin, CreateView):
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


class FilmCreateView(OnlyAdmin, CreateView):
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


class ProductDeleteView(OnlyAdmin, DeleteView):
    model = Product
    template_name = 'adminpanel/productDelete.html'
    success_url = '/adminpanel/products'


class BookUpdateView(OnlyAdmin, UpdateView):
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


class CDUpdateView(OnlyAdmin, UpdateView):
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


class FilmUpdateView(OnlyAdmin, UpdateView):
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


class UserDeleteView(OnlyAdmin, DeleteView):
    model = MyUser
    template_name = 'adminpanel/productDelete.html'
    success_url = '/adminpanel/users'


class UserUpdateView(OnlyAdmin, UpdateView):
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


class ChangeOrderStatus(OnlyAdmin, View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = self.request.POST['status']
        if self.request.POST['status'] == 'Extended':
            order.debt = order.total
            order.save()
        return redirect('OrdersListView')
