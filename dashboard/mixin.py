from django.shortcuts import redirect
from django.contrib import messages
from .forms import OrderStatus


class OnlyAdmin(object):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_anonymous and self.request.user.is_admin:
            return super().dispatch(*args, **kwargs)
        else:
            messages.success(self.request, 'Only for Admins')
            return redirect('home')


class OrderChangeStatusMixin(object):
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['status'] = OrderStatus
        return data
