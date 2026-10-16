from django.views.generic import ListView, DetailView
from .models import Producto


class ProductoInicioView(ListView):
    model = Producto
    template_name = 'productos/index.html'
    context_object_name = 'productos'
    paginate_by = 20


class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 20


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'