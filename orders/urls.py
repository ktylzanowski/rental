from django.urls import path
from .views import OrdersView, PayDebt, ReturnView

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='Orders'),
    path('orders/paydebt', PayDebt.as_view(), name='PayDebt'),
    path('orders/return', ReturnView.as_view(), name='ReturnView'),
]
