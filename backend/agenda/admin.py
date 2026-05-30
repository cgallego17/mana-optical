from django.contrib import admin

from .models import Reserva, Servicio


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
