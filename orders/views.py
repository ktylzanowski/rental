from orders.models import OrderItem, Order, Payment, Shipping
from django.shortcuts import redirect
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from products.models import Rental, Product, Genre, ProductIndex
from django.db.models import Prefetch
import json
from cart.cart import Cart
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from collections import defaultdict
from accounts.models import MyUser
from .forms import TimeSection
import datetime


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/orders.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            Prefetch('orderitem_set', OrderItem.objects.select_related('product'))
        ).filter(user=self.request.user).exclude(status='Returned')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        orders_extended = Order.objects.filter(user=self.request.user, status='Extended')
        price = 0
        for order in orders_extended:
            price += order.debt
        data['price'] = price
        return data


class OrdersArchiveView(ListView):
    model = Order
    template_name = "orders/ordersarchive.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            Prefetch('orderitem_set', OrderItem.objects.select_related('product'))
        ).filter(user=self.request.user, status='Returned')
        return qs


class PaymentListView(ListView):
    model = Payment
    template_name = "orders/paymentListView.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class OrderCreate(View):
    def get(self, request):
        success(request, "Your order was successful!")
        return redirect('home')

    def post(self, request):
        cart = Cart(request)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=cart.get_total_price(),
            status=body['status'],
        )
        payment.save()

        shipping = Shipping.objects.create(
            user=request.user,
            shipping_method=body['shipping'],
            if_paid=True,
            postage=body['shippingCost'],
            quantity_of_items=len(cart),
        )
        shipping.save()

        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now(),
            deadline=timezone.now()+timedelta(days=7),
            status="Ordered",
            total=cart.get_total_price(),
            payment=payment,
            shipping=shipping,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            phone=request.user.phone,
            city=request.user.city,
            zip_code=request.user.zip_code,
            street=request.user.street,
            building_number=request.user.building_number,
            apartment_number=request.user.apartment_number,
        )
        order.save()
        for item in cart:
            item['product'].popularity += 1
            item['product'].save()
            index = ProductIndex.objects.get(pk=item['index'])
            OrderItem.objects.create(
                product=item['product'],
                product_index=index,
                user=self.request.user,
                price=item['price'],
                order=order,
            )
        cart.clear()

        email_template = render_to_string('cart/email_payment_success.html', {})
        email = EmailMessage(
            'Payment Success',
            email_template,
            settings.EMAIL_HOST_USER,
            ['ktylzanowski@gmail.com'],
        )
        email.fail_silently = False
        email.send()
        return redirect('home')


class PayDebt(View):
    def get(self, request):
        success(request, "Your debt was paid!")
        return redirect('Orders')

    def post(self, request):
        orders = Order.objects.filter(user=request.user, status='Extended')

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=body['cost'],
            status='payment',
        )
        payment.save()

        for order in orders:
            order.status = 'Delivered'
            order.debt = 0
            order.save()

        return redirect("home")


class ReturnView(DetailView):
    model = Order
    template_name = 'orders/returntorental.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        rental = Rental.objects.all()
        data['rental_list'] = rental
        return data


class MakeReturn(View):

    def post(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = 'Returned'
        order.return_date = datetime.datetime.now()
        order.save()
        success(request, "Order returned")
        return redirect('home')


class Statistics(ListView):
    model = Product
    template_name = 'orders/statistics.html'
    ordering = ['-popularity']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = TimeSection
        if self.request.GET:
            t1 = self.request.GET['t1']
            t2 = self.request.GET['t2']
        else:
            t1 = datetime.datetime(2023, 3, 22)
            t2 = timezone.now()

        genre = Genre.objects.all()
        dictionary = defaultdict(dict)
        for g in genre:
            prod = OrderItem.objects.filter(product__genre=g,
                                            product__genre__category=g.category,
                                            order__order_date__range=(t1, t2)).count()
            dictionary[g.category][g.name] = prod
        data["pop"] = dictionary

        users_items = {}
        users = MyUser.objects.all()
        for user in users:
            books = OrderItem.objects.filter(user=user,
                                             order__order_date__range=(t1, t2),
                                             product__genre__category="book",
                                             ).count()
            cds = OrderItem.objects.filter(user=user,
                                           order__order_date__range=(t1, t2),
                                           product__genre__category="cd").count()
            films = OrderItem.objects.filter(user=user,
                                             order__order_date__range=(t1, t2),
                                             product__genre__category="film").count()

            tab = [books, films, cds]
            users_items[user.email] = tab
        data['users_items'] = users_items

        return data
