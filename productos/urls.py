<<<<<<< HEAD
=======
# productos/urls.py
"""URLs de la app productos — W08 (CRUD completo)."""
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
<<<<<<< HEAD
    path('', views.inicio, name='inicio'),
    path('lista/', views.ProductoListView.as_view(), name='lista'),
    path('nuevo/', views.ProductoCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='detalle'),
    path('<int:producto_id>/editar/', views.ProductoUpdateView.as_view(), name='editar'),
    path('<int:producto_id>/eliminar/', views.ProductoDeleteView.as_view(), name='eliminar'),
]
=======
    # Lectura (W07)
    path('',
         views.ProductoListView.as_view(),
         name='lista'),
    path('<int:producto_id>/',
         views.ProductoDetailView.as_view(),
         name='detalle'),
    # Escritura (W08) — descomentadas
    path('nuevo/',
         views.ProductoCreateView.as_view(),
         name='crear'),
    path('<int:producto_id>/editar/',
         views.ProductoUpdateView.as_view(),
         name='editar'),
    path('<int:producto_id>/eliminar/',
         views.ProductoDeleteView.as_view(),
         name='eliminar'),
]
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
