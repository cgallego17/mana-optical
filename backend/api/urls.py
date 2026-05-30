from django.urls import include, path

from .views import busqueda, health

urlpatterns = [
    path('health/', health, name='health'),
    path('busqueda/', busqueda, name='busqueda'),
    path('catalogo/', include('catalogo.urls')),
    path('agenda/', include('agenda.urls')),
    path('clientes/', include('clientes.urls')),
]
