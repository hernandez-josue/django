# ventas/urls.py
"""URLs de la app ventas — W07."""
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path(
        '',
        views.VentaListView.as_view(),
        name='inicio'
    ),
    path(
        '',
        views.VentaListView.as_view(),
        name='lista'
    ),
    path(
        '<int:venta_id>/',
        views.VentaDetailView.as_view(),
        name='detalle'
    ),

    # Escritura (W08) — pendientes de implementar
    # path('nueva/', views.crear_venta, name='crear'),
    # path('<int:venta_id>/eliminar/', views.VentaDeleteView.as_view(), name='eliminar'),
]
