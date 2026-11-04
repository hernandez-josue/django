"""Vistas de la app ventas."""

# ventas/views.py — imports necesarios
from decimal import ROUND_HALF_UP, Decimal
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.utils import timezone
from xhtml2pdf import pisa


def _ruta_local(url_path):
    '''Traduce /static/... o /media/... a un archivo en disco (o None).'''
    static_prefix = '/' + settings.STATIC_URL.lstrip('/')
    media_prefix = '/' + settings.MEDIA_URL.lstrip('/')

    if url_path.startswith(static_prefix):
        relativa = url_path[len(static_prefix):]
        if settings.STATIC_ROOT:
            candidata = Path(settings.STATIC_ROOT) / relativa
            if candidata.is_file():
                return candidata
        encontrada = finders.find(relativa)  # funciona sin collectstatic
        return Path(encontrada) if encontrada else None

    if url_path.startswith(media_prefix):
        raiz = Path(settings.MEDIA_ROOT).resolve()
        candidata = (raiz / url_path[len(media_prefix):]).resolve()
        # Evita salir de MEDIA_ROOT con rutas tipo ../
        if raiz in candidata.parents and candidata.is_file():
            return candidata
    return None


def _link_callback(uri, rel):
    '''xhtml2pdf llama a esta funcion por cada imagen/CSS del HTML.'''
    ruta = _ruta_local(unquote(urlparse(uri).path))
    return str(ruta) if ruta is not None else uri


def _logo_url(config):
    '''URL del logo solo si existe; si no, se omite sin romper el PDF.'''
    if not config.logo:
        return ''
    try:
        url = config.logo.url
    except ValueError:
        return ''
    if url.startswith(('http://', 'https://')):
        return url  # media externa (S3)
    return url if _ruta_local(unquote(urlparse(url).path)) else ''


def calcular_totales(subtotal, iva_porcentaje):
    '''Subtotal, IVA y total con 2 decimales (redondeo comercial).'''
    centavos = Decimal('0.01')
    subtotal = Decimal(subtotal).quantize(centavos, ROUND_HALF_UP)
    iva = (subtotal * Decimal(iva_porcentaje) / 100).quantize(centavos, ROUND_HALF_UP)
    return {'subtotal': subtotal, 'iva': iva, 'total_con_iva': subtotal + iva}


@login_required
def venta_pdf(request, venta_id):
    '''Genera y descarga la factura de una venta en PDF (motor: xhtml2pdf).'''
    venta = get_object_or_404(
        Venta.objects.select_related('cliente').prefetch_related(
            'detalles__producto__categoria'
        ),
        pk=venta_id,
    )
    config = ConfiguracionERP.get_instance()
    context = {
        'venta': venta,
        'config': config,
        'logo_url': _logo_url(config),
        'hoy': timezone.localdate(),
        **calcular_totales(venta.total, config.iva_porcentaje),
    }

    html_string = render_to_string('ventas/factura_pdf.html', context, request=request)

    buffer = BytesIO()
    resultado = pisa.CreatePDF(
        src=html_string,
        dest=buffer,
        encoding='utf-8',
        link_callback=_link_callback,
    )
    if resultado.err:
        return HttpResponse('No se pudo generar el PDF.', status=500)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{venta.pk:05d}.pdf"'
    return response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from .forms import DetalleVentaForm, VentaForm
from .models import DetalleVenta, Venta


def inicio(request):
    return render(request, 'ventas/index.html')


# Eliminar la función crear_venta de W08 y reemplazar por:

@login_required
@permission_required('ventas.add_venta', raise_exception=True)
def crear_venta(request):
    """Crea un encabezado de venta con una línea de detalle.

    Decoradores (se aplican de abajo hacia arriba):
        @login_required            → verifica autenticación
        @permission_required(...)  → verifica permiso add_venta

    GET  → muestra los dos formularios vacíos.
    POST → valida ambos, guarda si correctos, muestra errores si no.
    """
    venta_form   = VentaForm(request.POST or None)
    detalle_form = DetalleVentaForm(request.POST or None)

    if request.method == 'POST':
        if venta_form.is_valid() and detalle_form.is_valid():
            venta         = venta_form.save()
            detalle       = detalle_form.save(commit=False)
            detalle.venta = venta
            detalle.save()
            messages.success(
                request,
                f'Venta #{venta.pk} registrada. '
                f'Total: ${venta.total:.2f}'
            )
            return redirect('ventas:detalle', venta_id=venta.pk)

    return render(request, 'ventas/crear.html', {
        'venta_form':   venta_form,
        'detalle_form': detalle_form,
    })
    


class VentaListView(ListView):
    """Lista paginada de ventas en orden cronológico inverso."""

    model = Venta
    template_name = 'ventas/lista.html'
    context_object_name = 'ventas'
    paginate_by = 20

    def get_queryset(self):
        return Venta.objects.select_related('cliente').order_by('-fecha')
    
class VentaInicioView(VentaListView):
    """Página inicial: igual que la lista, pero con index.html."""

    template_name = 'ventas/index.html'


class VentaDetailView(DetailView):
    """Detalle de una venta con todas sus líneas de producto."""

    model = Venta
    template_name = 'ventas/detalle.html'
    context_object_name = 'venta'
    pk_url_kwarg = 'venta_id'

    def get_queryset(self):
        return (
            Venta.objects
            .select_related('cliente')
            .prefetch_related('detalles__producto')
        )


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    """Confirmación y borrado de una venta (y sus detalles en cascada)."""

    model = Venta
    template_name = 'ventas/eliminar.html'
    pk_url_kwarg = 'venta_id'
    success_url = reverse_lazy('ventas:lista')

    def form_valid(self, form):
        pk = self.object.pk
        response = super().form_valid(form)
        messages.success(self.request, f'Venta #{pk} eliminada.')
        return response