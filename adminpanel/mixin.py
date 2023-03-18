from .forms import OrderStatus


class StatusMixin(object):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['order_status'] = OrderStatus
        return data
