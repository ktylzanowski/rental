from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='Home'),
    path('books', views.BookListView.as_view(), name='BookListView'),
    path('films', views.FilmListView.as_view(), name='FilmListView'),
    path('cds', views.CDListView.as_view(), name='CDListView'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='ProductDetail'),
]
