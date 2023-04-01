from django.urls import path
from .views import OrdersView, PayDebt, ReturnView, OrdersArchiveView, MakeReturn, OrderCreate, Statistics, PaymentListView

urlpatterns = [
    path('', OrdersView.as_view(), name='Orders'),
    path('archive/', OrdersArchiveView.as_view(), name='OrdersArchive'),
    path('statics/', Statistics.as_view(), name='Statistics'),
    path('payments/', PaymentListView.as_view(), name='PaymentUserListView'),

    path('order-create/', OrderCreate.as_view(), name='OrderCreate'),
    path('pay-debt/', PayDebt.as_view(), name='PayDebt'),
    path('return/<int:pk>/', ReturnView.as_view(), name='ReturnView'),
    path('return/<int:pk>/<str:rental>/make-return/', MakeReturn.as_view(), name='MakeReturn'),
]
