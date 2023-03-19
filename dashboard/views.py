from .mixin import OnlyAdmin, OrderChangeStatusMixin
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from products.models import Book, CD, Film, Product
from orders.models import Order, Payment
from accounts.models import MyUser
from django.contrib.messages import success
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import datetime, timedelta


class Dashboard(OnlyAdmin, View):

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

        number_of_payments = len(Payment.objects.all())
        payments = Payment.objects.all()
        total_income = 0
        for payment in payments:
            total_income += int(payment.amount_paid)

        context = {'number_of_books': number_of_books, 'number_of_cds': number_of_cds,
                   'number_of_films': number_of_films, 'number_of_all_products': number_of_all_products,
                   'number_of_ordered': number_of_ordered, 'number_of_sent': number_of_sent,
                   'number_of_delivered': number_of_delivered, 'number_of_extended': number_of_extended,
                   'number_of_returned': number_of_returned, 'number_of_users': number_of_users,
                   'number_of_payments': number_of_payments, 'total_income': total_income}

        return render(request, 'dashboard/dashboard.html', context)


class ProductListView(OnlyAdmin, View):

    def get(self, request):
        books = Book.objects.all()
        cds = CD.objects.all()
        films = Film.objects.all()
        context = {'books': books, 'cds': cds, 'films': films}
        return render(request, 'dashboard/listview/productListView.html', context)


class BookCreateView(OnlyAdmin, CreateView):
    model = Book
    template_name = 'dashboard/forms/createProduct.html'
    success_url = '/dashboard/'

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
        success(self.request, 'Add Book')
        return super().form_valid(form)


class CDCreateView(OnlyAdmin, CreateView):
    model = CD
    template_name = 'dashboard/forms/createProduct.html'
    success_url = '/dashboard/'

    fields = [
        'title',
        'image',
        'quantity',
        'price',
        'band',
        'tracklist',
        'genre',
    ]

    def form_valid(self, form):
        success(self.request, 'Add CD')
        return super().form_valid(form)


class FilmCreateView(OnlyAdmin, CreateView):
    model = Film
    template_name = 'dashboard/forms/createProduct.html'
    success_url = '/dashboard/'

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
        success(self.request, 'Add Film')
        return super().form_valid(form)


class BookUpdateView(OnlyAdmin, UpdateView):
    model = Book
    template_name = 'dashboard/forms/update.html'
    success_url = '/dashboard/products'
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
    template_name = 'dashboard/forms/update.html'
    success_url = '/dashboard/products'
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
    template_name = 'dashboard/forms/update.html'
    success_url = '/dashboard/products'
    fields = [
        'title',
        'image',
        'quantity',
        'price',
        'director',
        'duration',
        'genre',
    ]


class ProductDeleteView(OnlyAdmin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        success(request, "Product deleted")
        return redirect('Dashboard')


class OrderListView(OnlyAdmin, OrderChangeStatusMixin, ListView):
    model = Order
    template_name = "dashboard/listview/orderListView.html"


class OrderDetailView(OnlyAdmin, OrderChangeStatusMixin, DetailView):
    model = Order
    template_name = 'dashboard/detailview/orderDetailView.html'


class ChangeStatus(OnlyAdmin, View):
    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = self.request.POST['status']
        if self.request.POST['status'] == 'Extended':
            order.debt += order.total
            order.deadline = order.deadline + timedelta(days=7)
        elif self.request.POST['status'] == 'Returned':
            order.return_date = timezone.now()
        order.save()
        success(request, 'The status has been changed')
        return redirect('OrderListView')


class UserListView(OnlyAdmin, ListView):
    model = MyUser
    template_name = 'dashboard/listview/userListView.html'
    ordering = ['-pk']


class UserUpdateView(OnlyAdmin, UpdateView):
    model = MyUser
    template_name = 'dashboard/forms/update.html'
    success_url = '/dashboard/users'
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

    def form_valid(self, form):
        success(self.request, "User information has been updated")
        return super().form_valid(form)


class UserDeleteView(OnlyAdmin, View):
    def get(self, request, pk):
        user = get_object_or_404(MyUser, pk=pk)
        user.delete()
        success(request, "User deleted")
        return redirect('Dashboard')


class PaymentListView(OnlyAdmin, ListView):
    model = Payment
    template_name = "dashboard/listview/paymentListView.html"
