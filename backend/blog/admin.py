from django.contrib import admin

from .models import CategoriaBlog, Post


@admin.register(CategoriaBlog)
class CategoriaBlogAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'slug',
        'categoria',
        'publicado',
        'publicado_en',
        'creado_en',
    )
    list_filter = ('publicado', 'categoria')
    search_fields = ('titulo', 'slug', 'extracto', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    ordering = ('-publicado_en', '-creado_en')
