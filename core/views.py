# core/views.py
"""Vistas principales del proyecto ERP — W02.

Migración: HttpResponse → render() con templates y contexto.
"""
from django.shortcuts import render
from django.urls import reverse


def bienvenida(request):
    """Página de inicio del ERP con tarjetas de módulos.

    Context:
        modulos (list): Lista de dicts con icono, nombre, url y descripcion.

    Returns:
        HttpResponse con template bienvenida.html.
    """
    modulos = [
        {
            'nombre': 'Productos',
            'icono': '📦',
            'url': reverse('productos:lista'),
            'descripcion': 'Inventario, precios y stock',
        },
        {
            'nombre': 'Clientes',
            'icono': '👥',
            'url': reverse('clientes:lista'),
            'descripcion': 'Cartera y gestión de clientes',
        },
        {
            'nombre': 'Proveedores',
            'icono': '🏭',
            'url': reverse('proveedores:lista'),
            'descripcion': 'Red de proveedores',
        },
        {
            'nombre': 'Ventas',
            'icono': '💰',
            'url': reverse('ventas:lista'),
            'descripcion': 'Pedidos, facturas y cobros',
        },
        {
            'nombre': 'Reportes',
            'icono': '📊',
            'url': reverse('reportes:inicio'),
            'descripcion': 'Dashboard y analítica',
        },
        {
            'nombre': 'Admin',
            'icono': '⚙️',
            'url': '/admin/',
            'descripcion': 'Panel de administración Django',
        },
    ]
    return render(request, 'bienvenida.html', {'modulos': modulos})


# PRUEBA TEMPORAL DEL REPORTE DIARIO
import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods

logger_reporte = logging.getLogger(__name__)


@staff_member_required
@require_http_methods(["GET", "POST"])
def probar_reporte_ventas(request):
    resultado = None
    error = None

    if request.method == "POST":
        try:
            from ventas.tasks import reporte_ventas_diario
            resultado = reporte_ventas_diario.run()
        except Exception:
            logger_reporte.exception("Error ejecutando reporte de ventas")
            error = "Error al generar el reporte. Revisa los logs de Render."

    return render(
        request,
        "admin/reporte_prueba.html",
        {"resultado": resultado, "error": error},
    )
