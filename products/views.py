from django.views.generic import ListView, DetailView
from products.models import Product


class Home(ListView):
    template_name = 'products/home.html'

    def get_queryset(self):
        queryset = Product.objects.all().order_by('title')
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detailview.html'
