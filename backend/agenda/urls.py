from django.urls import path

from .views import (
    AdminHorarioDetailView,
    AdminHorarioListView,
    AdminReservaDetailView,
    AdminReservaListView,
    AdminServicioDetailView,
    AdminServicioListCreateView,
    DisponibilidadView,
    HorarioListView,
    ReservaCreateView,
    ServicioListView,
)

urlpatterns = [
    path('servicios/', ServicioListView.as_view(), name='agenda_servicios_list'),
    path('horarios/', HorarioListView.as_view(), name='agenda_horarios_list'),
    path('disponibilidad/', DisponibilidadView.as_view(), name='agenda_disponibilidad'),
    path('reservas/', ReservaCreateView.as_view(), name='agenda_reservas_create'),

    path('admin/reservas/', AdminReservaListView.as_view(), name='admin_agenda_reservas_list'),
    path('admin/reservas/<int:pk>/', AdminReservaDetailView.as_view(), name='admin_agenda_reservas_detail'),
    path('admin/servicios/', AdminServicioListCreateView.as_view(), name='admin_agenda_servicios_list_create'),
    path('admin/servicios/<int:pk>/', AdminServicioDetailView.as_view(), name='admin_agenda_servicios_detail'),
    path('admin/horarios/', AdminHorarioListView.as_view(), name='admin_agenda_horarios_list'),
    path('admin/horarios/<int:pk>/', AdminHorarioDetailView.as_view(), name='admin_agenda_horarios_detail'),
]
