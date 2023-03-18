from django.urls import path
from .views import OrdersView, PayDebt, ReturnView, OrdersArchiveView, MakeReturn

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='Orders'),
    path('orders/archive', OrdersArchiveView.as_view(), name='OrdersArchive'),
    path('orders/paydebt', PayDebt.as_view(), name='PayDebt'),
    path('orders/return/<int:pk>', ReturnView.as_view(), name='ReturnView'),
    path('orders/return/<int:pk>/makereturn', MakeReturn.as_view(), name='MakeReturn'),
]
