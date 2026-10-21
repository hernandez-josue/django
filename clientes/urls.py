<<<<<<< HEAD
=======
# clientes/urls.py
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
<<<<<<< HEAD
    path('', views.inicio, name='inicio'),
    path('lista/', views.ClienteListView.as_view(), name='lista'),
    path('nuevo/', views.ClienteCreateView.as_view(), name='crear'),
    path('<int:cliente_id>/', views.ClienteDetailView.as_view(), name='detalle'),
    path('<int:cliente_id>/editar/', views.ClienteUpdateView.as_view(), name='editar'),
    path('<int:cliente_id>/eliminar/', views.ClienteDeleteView.as_view(), name='eliminar'),
=======
    path('',                          views.ClienteListView.as_view(),   name='lista'),
    path('<int:cliente_id>/',         views.ClienteDetailView.as_view(), name='detalle'),
    path('nuevo/',                    views.ClienteCreateView.as_view(), name='crear'),
    path('<int:cliente_id>/editar/',  views.ClienteUpdateView.as_view(), name='editar'),
    path('<int:cliente_id>/eliminar/',views.ClienteDeleteView.as_view(), name='eliminar'),
>>>>>>> 996cf3682ecfbde6bde1ae2b7bcaaf6092ce5077
]