from django.shortcuts import render
from django.views.generic import View, ListView
from orders.models import Order, OrderItem


class AdminPanel(View):

    def get(self, request):
        orders = Order.objects.order_by('-order_date')[:5]
        return render(request, 'adminpanel/adminpanel.html', {'orders': orders})

    def post(self):
        pass


class OrderListView(ListView):
    model = Order
    template_name = 'adminpanel/ordersListView.html'
    ordering = ['-pk']
