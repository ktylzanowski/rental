from .forms import OrderStatus
from django.shortcuts import redirect
from django.contrib import messages


class OnlyAdmin(object):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_anonymous and self.request.user.is_admin:
            return super().dispatch(*args, **kwargs)
        else:
            messages.success(self.request, 'Only for Admins')
            return redirect('home')


class StatusMixin(object):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['order_status'] = OrderStatus
        return data
