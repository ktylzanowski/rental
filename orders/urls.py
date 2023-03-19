from django.urls import path
from .views import OrdersView, PayDebt, ReturnView, OrdersArchiveView, MakeReturn, OrderCreate, Statistics

urlpatterns = [
    path('', OrdersView.as_view(), name='Orders'),
    path('statics/', Statistics.as_view(), name='Statistics'),
    path('archive/', OrdersArchiveView.as_view(), name='OrdersArchive'),
    path('ordercreate/', OrderCreate.as_view(), name='OrderCreate'),
    path('paydebt/', PayDebt.as_view(), name='PayDebt'),
    path('return/<int:pk>/', ReturnView.as_view(), name='ReturnView'),
    path('return/<int:pk>/makereturn/', MakeReturn.as_view(), name='MakeReturn'),
]
