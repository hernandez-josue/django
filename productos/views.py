# productos/views.py — actualizar el import al inicio:
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import ListView, DetailView
from .models import Producto
from django.shortcuts import render

def inicio(request):
    return render(request, 'productos/index.html')

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

    # productos/views.py — agregar los imports al inicio del archivo:
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import ProductoForm


class ProductoCreateView(LoginRequiredMixin, CreateView):
    """Formulario para crear un nuevo producto.

    LoginRequiredMixin PRIMERO en la herencia (obligatorio).
    Redirige a /accounts/login/ si el usuario no está autenticado.
    """

    model         = Producto
    form_class    = ProductoForm
    template_name = 'productos/crear.html'
    success_url   = reverse_lazy('productos:lista')  # reverse_lazy (no reverse)

    def form_valid(self, form):
        """Agrega mensaje flash de éxito al guardar."""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Producto "{self.object.nombre}" creado exitosamente.'
        )
        return response


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    """Formulario para editar un producto existente."""

    model         = Producto
    form_class    = ProductoForm
    template_name = 'productos/editar.html'
    pk_url_kwarg  = 'producto_id'
    success_url   = reverse_lazy('productos:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Producto "{self.object.nombre}" actualizado.'
        )
        return response


# Reemplazar la clase ProductoDeleteView:


class ProductoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/eliminar.html'
    pk_url_kwarg = 'producto_id'
    success_url = reverse_lazy('productos:lista')
    permission_required = 'productos.delete_producto'
   

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f'Producto "{nombre}" eliminado.')
        return response

# ── Exportación a Excel (W12) ─────────────────────────────────────
from django.contrib.auth.decorators import login_required as _login_required
from django.http import HttpResponse as _HttpResponse
from openpyxl import Workbook as _Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


@_login_required
def exportar_excel(request):
    wb = _Workbook()
    ws = wb.active
    ws.title = 'Productos'
    ws.append(['ID', 'Nombre', 'Categoria', 'Precio', 'Stock'])
    for p in Producto.objects.select_related('categoria').order_by('nombre'):
        ws.append([
            p.pk,
            p.nombre,
            p.categoria.nombre if p.categoria else '',
            float(p.precio),
            p.stock,
        ])

    # Encabezados: azul con letra blanca y negrita
    relleno = PatternFill('solid', start_color='0A2342')
    for celda in ws[1]:
        celda.font = Font(bold=True, color='FFFFFF')
        celda.fill = relleno
        celda.alignment = Alignment(horizontal='center')

    # Precio con formato de dinero
    for fila in ws.iter_rows(min_row=2, min_col=4, max_col=4):
        for celda in fila:
            celda.number_format = '$#,##0.00'

    # Encabezado fijo y filtros
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions

    # Ancho de columna segun el contenido
    for i, columna in enumerate(ws.columns, start=1):
        ancho = max(len(str(c.value)) if c.value is not None else 0 for c in columna)
        ws.column_dimensions[get_column_letter(i)].width = min(ancho + 3, 50)

    response = _HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
    wb.save(response)
    return response
