from django.urls import path

from .views import (
    AdminExcepcionDetailView,
    AdminExcepcionListCreateView,
    AdminHorarioDetailView,
    AdminHorarioListView,
    AdminReservaDetailView,
    AdminReservaListView,
    AdminServicioDetailView,
    AdminServicioExcepcionDetailView,
    AdminServicioExcepcionListCreateView,
    AdminServicioListCreateView,
    DisponibilidadView,
    ExcepcionListView,
    HorarioListView,
    ReservaCreateView,
    ServicioExcepcionListView,
    ServicioListView,
)

urlpatterns = [
    path('servicios/', ServicioListView.as_view(), name='agenda_servicios_list'),
    path('horarios/', HorarioListView.as_view(), name='agenda_horarios_list'),
    path('excepciones/', ExcepcionListView.as_view(), name='agenda_excepciones_list'),
    path('servicios/excepciones/', ServicioExcepcionListView.as_view(), name='agenda_servicio_excepciones_list'),
    path('disponibilidad/', DisponibilidadView.as_view(), name='agenda_disponibilidad'),
    path('reservas/', ReservaCreateView.as_view(), name='agenda_reservas_create'),

    path('admin/reservas/', AdminReservaListView.as_view(), name='admin_agenda_reservas_list'),
    path('admin/reservas/<int:pk>/', AdminReservaDetailView.as_view(), name='admin_agenda_reservas_detail'),
    path('admin/servicios/', AdminServicioListCreateView.as_view(), name='admin_agenda_servicios_list_create'),
    path('admin/servicios/<int:pk>/', AdminServicioDetailView.as_view(), name='admin_agenda_servicios_detail'),
    path(
        'admin/servicios/excepciones/',
        AdminServicioExcepcionListCreateView.as_view(),
        name='admin_agenda_servicio_excepciones_list_create',
    ),
    path(
        'admin/servicios/excepciones/<int:pk>/',
        AdminServicioExcepcionDetailView.as_view(),
        name='admin_agenda_servicio_excepciones_detail',
    ),
    path('admin/horarios/', AdminHorarioListView.as_view(), name='admin_agenda_horarios_list'),
    path('admin/horarios/<int:pk>/', AdminHorarioDetailView.as_view(), name='admin_agenda_horarios_detail'),
    path('admin/excepciones/', AdminExcepcionListCreateView.as_view(), name='admin_agenda_excepciones_list_create'),
    path('admin/excepciones/<int:pk>/', AdminExcepcionDetailView.as_view(), name='admin_agenda_excepciones_detail'),
]
