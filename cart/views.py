from django.views.generic import View, ListView
from .models import CartItem, Cart
from orders.models import Order, OrderItem, Payment, Shipping, ShippingMethod
from products.models import Product
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
import json
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import timedelta


class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'cart/cart.html'

    def user_cart(self):
        user_cart, created = Cart.objects.get_or_create(
            user=self.request.user,
        )
        user_cart.save()
        return user_cart

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(cart=self.user_cart())
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['price'] = self.user_cart().total
        return data


class CheckoutView(LoginRequiredMixin, View):

    def get(self, request):
        success(request, "Your order was successful!")
        return redirect('home')

    def post(self, request):
        user_cart = Cart.objects.get(user=request.user)
        items_in_cart = CartItem.objects.filter(cart=user_cart)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        payment = Payment.objects.create(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            amount_paid=user_cart.total(),
            status=body['status'],
        )
        payment.save()

        shipping_method = ShippingMethod.objects.get(name=body['shipping'])

        shipping = Shipping.objects.create(
            user=request.user,
            shipping_method=shipping_method,
            if_paid=True,
            postage=shipping_method.price,
            quantity_of_items=1,
        )
        shipping.save()

        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now(),
            return_date=timezone.now()+timedelta(days=7),
            status="Ordered",
            total=user_cart.total(),
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

        for item in items_in_cart:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                user=request.user,
            ).save()

        CartItem.objects.filter(cart=user_cart).delete()
        Cart.objects.get(user=request.user).delete()

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


class DeleteItemView(LoginRequiredMixin, View):

    def post(self, request, pk):
        item_to_removed = CartItem.objects.get(pk=pk)

        item = Product.objects.get(pk=item_to_removed.product.pk)
        item.quantity += 1

        if not item.is_available:
            item.is_available = True
        item.save()
        item_to_removed.delete()
        success(self.request, "Item Deleted")
        return redirect("Cart")


