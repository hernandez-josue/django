<<<<<<< HEAD
=======
# proveedores/urls.py
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
<<<<<<< HEAD
    path('', views.inicio, name='inicio'),
    path('lista/', views.ProveedorListView.as_view(), name='lista'),
    path('nuevo/', views.ProveedorCreateView.as_view(), name='crear'),
    path('<int:proveedor_id>/', views.ProveedorDetailView.as_view(), name='detalle'),
    path('<int:proveedor_id>/editar/', views.ProveedorUpdateView.as_view(), name='editar'),
    path('<int:proveedor_id>/eliminar/', views.ProveedorDeleteView.as_view(), name='eliminar'),
=======
    path('',                            views.ProveedorListView.as_view(),   name='lista'),
    path('<int:proveedor_id>/',         views.ProveedorDetailView.as_view(), name='detalle'),
    path('nuevo/',                      views.ProveedorCreateView.as_view(), name='crear'),
    path('<int:proveedor_id>/editar/',  views.ProveedorUpdateView.as_view(), name='editar'),
    path('<int:proveedor_id>/eliminar/',views.ProveedorDeleteView.as_view(), name='eliminar'),
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
]