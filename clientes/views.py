
"""
Vistas de la aplicación clientes.
Incluye listado, detalle y operaciones CRUD.
"""
from django.shortcuts import render

def inicio(request):
    return render(request, 'clientes/index.html')






from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Cliente
from .forms import ClienteForm


class ClienteInicioView(ListView):
    """Página inicial con el listado de clientes."""

    model = Cliente
    template_name = "clientes/index.html"
    context_object_name = "clientes"
    paginate_by = 20


class ClienteListView(ListView):
    """Muestra los clientes registrados."""

    model = Cliente
    template_name = "clientes/lista.html"
    context_object_name = "clientes"
    paginate_by = 20


class ClienteDetailView(DetailView):
    """Muestra los datos de un cliente."""

    model = Cliente
    template_name = "clientes/detalle.html"
    context_object_name = "cliente"
    pk_url_kwarg = "cliente_id"


class ClienteCreateView(LoginRequiredMixin, CreateView):
    """Formulario para registrar un cliente."""

    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/crear.html"
    success_url = reverse_lazy("clientes:lista")

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            f'Cliente "{self.object.nombre}" creado exitosamente.'
        )

        return response


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """Formulario para editar un cliente existente."""

    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/editar.html"
    pk_url_kwarg = "cliente_id"
    success_url = reverse_lazy("clientes:lista")

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            f'Cliente "{self.object.nombre}" actualizado.'
        )

        return response


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """Confirma y elimina un cliente."""

    model = Cliente
    template_name = "clientes/eliminar.html"
    pk_url_kwarg = "cliente_id"
    success_url = reverse_lazy("clientes:lista")

    def form_valid(self, form):
        nombre = self.object.nombre

        response = super().form_valid(form)

        messages.success(
            self.request,
            f'Cliente "{nombre}" eliminado.'
        )

        return response
