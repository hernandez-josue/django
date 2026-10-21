<<<<<<< HEAD
=======
# ventas/urls.py
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
<<<<<<< HEAD
    path('', views.inicio, name='inicio'),
    path('lista/', views.VentaListView.as_view(), name='lista'),
    path('nueva/', views.crear_venta, name='crear'),
    path('<int:venta_id>/', views.VentaDetailView.as_view(), name='detalle'),
    path('<int:venta_id>/eliminar/', views.VentaDeleteView.as_view(), name='eliminar'),
=======
    path('',                        views.VentaListView.as_view(),  name='lista'),
    path('<int:venta_id>/',         views.VentaDetailView.as_view(),name='detalle'),
    path('nueva/',                  views.crear_venta,              name='crear'),
    path('<int:venta_id>/eliminar/',views.VentaDeleteView.as_view(),name='eliminar'),
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
]