from django.views.generic import ListView, DetailView
from .models import Cliente


class ClienteInicioView(ListView):
    model = Cliente
    template_name = 'clientes/index.html'
    context_object_name = 'clientes'
    paginate_by = 20


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/detalle.html'
    context_object_name = 'cliente'
    pk_url_kwarg = 'cliente_id'

    