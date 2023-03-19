from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='Dashboard'),

    path('products/', views.ProductListView.as_view(), name='ProductListView'),
    path('products/<int:pk>/update-book', views.BookUpdateView.as_view(), name='BookUpdateView'),
    path('products/<int:pk>/update-cd', views.CDUpdateView.as_view(), name='CDUpdateView'),
    path('products/<int:pk>/update-film', views.FilmUpdateView.as_view(), name='FilmUpdateView'),
    path('products/<int:pk>/delete', views.ProductDeleteView.as_view(), name='ProductDeleteView'),
    path('products/add-book', views.BookCreateView.as_view(), name='BookCreateView'),
    path('products/add-cd', views.BookCreateView.as_view(), name='CDCreateView'),
    path('products/add-film', views.BookCreateView.as_view(), name='FilmCreateView'),

    path('orders/', views.OrderListView.as_view(), name="OrderListView"),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name="OrderDetailView"),
    path('orders/<int:pk>/change-status', views.ChangeStatus.as_view(), name='ChangeStatus'),

    path('users/', views.UserListView.as_view(), name="UserListView"),
    path('users/<int:pk>/update', views.UserUpdateView.as_view(), name="UserUpdateView"),
    path('users/<int:pk>/delete', views.UserDeleteView.as_view(), name="UserDeleteView"),

    path('payment/', views.PaymentListView.as_view(), name="PaymentListView"),
]
