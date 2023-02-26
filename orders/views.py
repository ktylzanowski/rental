from orders.models import OrderItem
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class OrdersView(LoginRequiredMixin, View):
    model = OrderItem
    template_name = "registration/orders.html"

    def get(self, request):
        obj = OrderItem.objects.filter(user=request.user)
        context = {'object_list': obj}
        return render(request, "orders/orders.html", context)
