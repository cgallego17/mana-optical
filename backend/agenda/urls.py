from django.urls import path

from .views import DisponibilidadView, ReservaCreateView, ServicioListView

urlpatterns = [
    path(
        'servicios/',
        ServicioListView.as_view(),
        name='agenda_servicios_list',
    ),
    path(
        'disponibilidad/',
        DisponibilidadView.as_view(),
        name='agenda_disponibilidad',
    ),
    path(
        'reservas/',
        ReservaCreateView.as_view(),
        name='agenda_reservas_create',
    ),
]
