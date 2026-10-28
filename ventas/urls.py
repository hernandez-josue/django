from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
   path('', views.VentaInicioView.as_view(), name='inicio'),
    path('lista/', views.VentaListView.as_view(), name='lista'),
    path('nueva/', views.crear_venta, name='crear'),
    path('<int:venta_id>/', views.VentaDetailView.as_view(), name='detalle'),
    path('<int:venta_id>/eliminar/', views.VentaDeleteView.as_view(), name='eliminar'),
]