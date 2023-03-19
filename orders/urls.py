from django.urls import path
from .views import OrdersView, PayDebt, ReturnView, OrdersArchiveView, MakeReturn, OrderCreate, Statistics

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='Orders'),
    path('orders/statics', Statistics.as_view(), name='Statistics'),
    path('orders/archive', OrdersArchiveView.as_view(), name='OrdersArchive'),
    path('orders/ordercreate', OrderCreate.as_view(), name='OrderCreate'),
    path('orders/paydebt', PayDebt.as_view(), name='PayDebt'),
    path('orders/return/<int:pk>', ReturnView.as_view(), name='ReturnView'),
    path('orders/return/<int:pk>/makereturn', MakeReturn.as_view(), name='MakeReturn'),
]
