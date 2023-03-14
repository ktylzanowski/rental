from django.urls import path
from .views import OrdersView, PayDebt, order_complete

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='Orders'),
    path('orders/paydebt', PayDebt.as_view(), name='PayDebt'),
    path('orders/paydebt/complete', order_complete, name='CompletePayDebt')
]
