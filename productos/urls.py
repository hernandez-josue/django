"""URLs de la app productos — W07."""

from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path(
        '',
        views.ProductoInicioView.as_view(),
        name='inicio'
    ),
    path(
        'lista/',
        views.ProductoListView.as_view(),
        name='lista'
    ),
    path(
        '<int:pk>/',
        views.ProductoDetailView.as_view(),
        name='detalle'
    ),
]