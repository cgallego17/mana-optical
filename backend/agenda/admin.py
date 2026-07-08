from django.contrib import admin

from .models import DiaExcepcion, HorarioAtencion, Reserva, Servicio


@admin.register(HorarioAtencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'abierto', 'hora_inicio', 'hora_fin')
    list_editable = ('abierto', 'hora_inicio', 'hora_fin')


@admin.register(DiaExcepcion)
class DiaExcepcionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'abierto', 'hora_inicio', 'hora_fin', 'motivo')
    list_filter = ('abierto',)
    date_hierarchy = 'fecha'


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'duracion_minutos', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha',
        'hora',
        'cliente',
        'nombre',
        'telefono',
        'estado',
        'servicio',
    )
    list_filter = ('estado', 'fecha', 'servicio')
    search_fields = ('nombre', 'telefono', 'email')
