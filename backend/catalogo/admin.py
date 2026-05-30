from django.contrib import admin

from .models import Categoria, Marca, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo', 'precio', 'categoria', 'marca')
    list_filter = ('activo', 'categoria', 'marca')
    search_fields = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
