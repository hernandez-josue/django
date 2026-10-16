"""URLs de la app clientes — W07."""

from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path(
        '',
        views.ClienteInicioView.as_view(),
        name='inicio'
    ),
    path(
        'lista/',
        views.ClienteListView.as_view(),
        name='lista'
    ),
    path(
        '<int:cliente_id>/',
        views.ClienteDetailView.as_view(),
        name='detalle'
    ),
]