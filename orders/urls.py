from django.urls import path
from .views import OrdersView, PayDebt

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='Orders'),
    path('orders/paydebt', PayDebt.as_view(), name='PayDebt'),
]
