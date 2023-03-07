from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from orders.models import Order
from cart.models import Cart, CartItem
from accounts.models import MyUser
from products.models import Product

class AdminPanel(View):

    def get(self, request):
        orders = Order.objects.order_by('-order_date')[:5]
        carts = Cart.objects.filter()[:5]
        context = {'orders': orders, 'carts': carts}
        return render(request, 'adminpanel/adminpanel.html', context)

    def post(self):
        pass


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
