from django.urls import path

from .views import AdminReservaListView, DisponibilidadView, ReservaCreateView, ServicioListView

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
    path(
        'admin/reservas/',
        AdminReservaListView.as_view(),
        name='admin_agenda_reservas_list',
    ),
]
